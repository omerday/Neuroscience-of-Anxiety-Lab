from medoc_api import tsa_device
from medoc_api import enums
# import tkinter as tk
# import tkinter.messagebox as tkmb
import time
from psychopy import core, visual, event, gui


def initiate_medoc_device():
    messagebox = gui.Dlg(title="Initialization Warning")
    messagebox.addText("Medoc device is initializing, please make sure the patient isn't connected to the thermode and press OK")
    messagebox.show()
    if not messagebox.OK:
        core.quit()

    device = tsa_device.TsaDevice(auto_connect_port=True)
    print("Connecting")
    device.start_status_thread(0.1)
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

def deliver_pain(window:visual.Window, temp, device):
    print(f"{round(time.time(), 2)} - Starting heat raise")
    print(f"State before Heat Increase = {device.status_state}")
    print(f"Temp before Heat Increase = {device.status_temp}")
    device.finite_ramp_by_temperature(temp, 0.1, 0.1, is_stop_on_response_unit_yes=False, time=500)
    print(f"State after Heat Increase = {device.status_state}")
    print(f"Temp after Heat Increase = {device.status_temp}")
    device.run_test()
    device.stop_test()

    print(f"{round(time.time(), 2)} - Staying for 4 sec")
    print(f"State before Heat Command = {device.status_state}")
    print(f"Temp before Heat Command = {device.status_temp}")
    device.finite_ramp_by_temperature(temp, 0.1, 0.1, is_stop_on_response_unit_yes=False, time=4000)
    device.run_test()
    device.stop_test()
    print(f"State After Heat Command = {device.status_state}")
    print(f"Temp After Heat Command = {device.status_temp}")

    print(f"{round(time.time(), 2)} - lowering to baseline")
    device.finite_ramp_by_temperature(32, 0.1, 0.1, is_stop_on_response_unit_yes=False, time=500)
    print(f"State before Return to Baseline = {device.status_state}")
    print(f"Temp before Return to Baseline = {device.status_temp}")
    device.run_test()
    print(f"State after Return to Baseline = {device.status_state}")
    print(f"Temp after Return to Baseline = {device.status_temp}")
    # lowering_test_start = time.time()
    # while device.status_temp > 32.5 and time.time() <= lowering_test_start + 4:
    #     print(f"Current Temperature: {device.status_temp}")
    #     core.wait(0.5)
    device.stop_test()


def cool_down(device):
    device.end_test()
    device.stop_status_thread()
    device.finalize()
    core.quit()