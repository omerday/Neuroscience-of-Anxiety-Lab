from medoc_api import tsa_device
from medoc_api import enums
import time
import csv

from datetime import datetime
from psychopy import core, visual, event, gui


def initiate_medoc_device():
    messagebox = gui.Dlg(title="Initialization Warning")
    messagebox.addText("Medoc device is initializing, please make sure the patient isn't connected to the thermode and press OK")
    messagebox.show()
    if not messagebox.OK:
        core.quit()

    device = tsa_device.TsaDevice(auto_connect_port=True)
    print("Connecting")
    device.start_status_thread(0.01)
    device.event_status_updated.connect(on_status_event)

    print("Initializing and Self-Test")
    device.enable_thermode(enums.ThermodeType.DCHEPS)
    device.set_active_thermode(enums.ThermodeType.DCHEPS)

    set_rest_mode_res = device.set_tcu_state(enums.SystemState.RestMode, run_self_test=True, wait_for_state=True)
    i = 0
    while set_rest_mode_res is None and i < 3:
        set_rest_mode_res = device.set_tcu_state(enums.SystemState.RestMode, run_self_test=True, wait_for_state=True)
        i += 1
    if set_rest_mode_res is None:
        print("Failed to send RestMode (SelfTest) request, exiting")
        device.finalize()
        exit()
    print("Self-Test finished")
    print("Going into TestInit mode")
    device.set_tcu_state(enums.SystemState.TestInit, run_self_test=True, wait_for_state=True)
    return device

def on_status_event(status_res):
    on_status_event.statuses.append(status_res)

class Proxy:
    def __init__(self, callback) -> None:
        self.callback = callback

    def handler(self, status_res):
        self.callback(status_res)

on_status_event.statuses = []

def log_temperaturs_to_csv(temperatures_csv_file, temperatures_line):
    # gets temperatures_csv_filename,temperatures_line and appends it to the csv file
    with open(temperatures_csv_file, mode='a', newline='', encoding='utf-8') as temperatures_csv:
        writer = csv.writer(temperatures_csv)
        temperatures_csv.seek(0, 2)
        if temperatures_csv.tell()==0:
            writer.writerow(["Timestamp", "Main Temp.", "Water Temp.", ])
        temperatures_list = temperatures_line.split("|")

        cleaned_temp_list = [item.split(":-")[1].strip() if ":-" in item else item for item in temperatures_list]
        writer.writerow(cleaned_temp_list)

def print_statuses():
    if len(on_status_event.statuses) == 0:
        pass
    start_time = on_status_event.statuses[0].m_timestamp
    for status in on_status_event.statuses :
        curr_time = status.m_timestamp
        for temp in status.m_heaterTemperature:
            status_time = curr_time - start_time
            message = f"Timestamp:- {status_time} " \
                  f"| Temperature:- {temp} " \
                  f"| Water:- {status.m_waterTemperature}"
            log_temperaturs_to_csv("temperatures_csv_file.csv", message)
            curr_time += 4

def deliver_pain(window:visual.Window, temp, device, params:dict):
    on_status_event.statuses.clear()
    start_time = time.time()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S.%f")
    
    print(current_time, " : 47 - heatHandler - ", f"{round(time.time() - start_time, 2)} - Raising to temp {temp}", " Ramp Time=", params['tempRampUpTime'], "\n")
    device.erase_conditional_events()
    tokens = []
    temperatures = []
    resp = device.finite_ramp_by_temperature(temp, 0.1, 0.1, is_stop_on_response_unit_yes=False, time = params['tempRampUpTime'])
    device.conditional_event(enums.EventCondition.TemperatureRaise, int(temp-1))
    tokens.append(resp.command_token)
    temperatures.append(temp)
    #-------------------------------------------------------------------------------
    #---------------- DZ: changing the finite ramp  by time to 5500 ----------------
    #----------------     instead of 4000 to see if it will add 1.5 sec ------------
    #----------------     in    average to meet 4 sec requirement       ------------
    #-------------------------------------------------------------------------------
    resp = device.finite_ramp_by_time(temp, time = 4000)
    tokens.append(resp.command_token)
    temperatures.append(temp)

    resp = device.finite_ramp_by_temperature(32, 0.1, 0.1, is_stop_on_response_unit_yes=False, time = params['tempRampUpTime'])
    device.conditional_event(enums.EventCondition.TemperatureDrop, 33)
    temperatures.append(32)
    tokens.append(resp.command_token)

    state_before_run = device.status_state
    temp_before_run = device.status_temp
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S.%f")
    print(current_time, f" : 106 - heatHandler - State before run_test = {state_before_run}")
    print(current_time, f" : 107 - heatHandler - Temp before run_test = {temp_before_run}")
    device.run_test()
            
    test_ongoing = True
    loop_round = 0
    temp_condition = temp - 0.1
    lowering_temp = False
    # wait for test finished
    while test_ongoing == True:
        time.sleep(0.5)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S.%f")
        loop_round = loop_round + 1
        temp_while_run = device.status_temp
        print(current_time, f" : 126 - heatHandler - Temp while run_test = ", temp_while_run, " Loop round= ", loop_round, " temp condititon=", temp_condition, '\n')
        if not lowering_temp and temp_while_run > temp_condition:
            temp_condition  = temp_before_run
            lowering_temp = True
        if lowering_temp and temp_while_run < temp_before_run:
            test_ongoing = False
            device.stop_test()
    print_statuses()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S.%f")
    print(current_time, f" : 131 - heatHandler - Temp after stop and end_test = {device.status_temp}")
    print(current_time, f" : 132 - heatHandler - State after stop and end_test = {device.status_state}")
    print(current_time, " : 133 - heatHandler - Elapsed time since start: ", f"{round(time.time() - start_time, 2)} - till end", "\n")

def cool_down(device):
    device.end_test()
    device.stop_status_thread()
    device.finalize()
    core.quit()
