from medoc_api.tsa_device import TsaDevice
import logging
import sys
import os
import medoc_api.enums as enums
import tkinter as tk
from tkinter import messagebox
import time
import csv

if sys.platform == "win32":
    from msvcrt import getch, getche
else:
    from getch import getch, getche

def __setup_logger(log_to_stdout=False, level=logging.DEBUG):
    logging.basicConfig(filename="log.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.NOTSET)

    if not log_to_stdout:
        return

    root = logging.getLogger()
    root.setLevel(logging.NOTSET)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

class TestRamp:

    def __init__(self, append=False) -> None:
        """
        :param append: Whether to append to the csv file or to rewrite it fully.
        """
    
    
    def run(self, num_tests=2):
        """
        Starts the test and finalizes at the end.

        :param num_tests: The number of times to run the procedure
        """

        self.test_ongoing = False
        print("Initializing")
        self.device_app = TsaDevice(auto_connect_port=False)  # Create device. It will establish a serial connection
        self.device_app.start_status_thread(0.01)
        self.device_app.event_status_updated.connect(self._on_status_event)

        print("Beginning Self-Test")
        #self.device_app.enable_thermode()
        self.device_app.enable_thermode(enums.ThermodeType.TSA)
        self.device_app.set_active_thermode(enums.ThermodeType.TSA)
        self.device_app.set_current_thermode(enums.DEVICE_TAG.Master)
        
        def check_condition():
            # Replace this condition with your own condition
            condition = True  # Example condition
            if condition:
                messagebox.showinfo("Please remove the thermode from the patient's skin", "Condition is satisfied!")
            else:
                messagebox.showwarning("Warning", "Condition is not satisfied!")
                root.destroy()
            # Create the main application window
            root = tk.Tk()
            root.title("Thermode is removed from patient's skin")

            # Button to check the condition
            check_button = tk.Button(root, text="OK, I have removed the thermode from the patient's skin", command=check_condition)
            check_button.pack(pady=20)
            root.mainloop()
            self.device_app.set_tcu_state(enums.SystemState.RestMode, run_self_test=True, wait_for_state=True)
            self.device_app.set_tcu_state(enums.SystemState.TestInit, wait_for_state=True)
            print("Self-Test finished")

    


        self.device_app.set_tcu_state(enums.SystemState.RestMode, run_self_test=True, wait_for_state=True)
        self.device_app.set_tcu_state(enums.SystemState.TestInit, wait_for_state=True)
        print("Self-Test finished")

        # clear conditional events from device and add new start test event
        self.device_app.erase_conditional_events()
        self.device_app.conditional_event(enums.EventCondition.Unconditional, 2)

        self.temperatures = [50, 20, 40, 30]
        self.tokens = []

        # send temperature commands to device and store command tokens
        for temperature in self.temperatures:
            r = self.device_app.finite_ramp_by_temperature(temperature, 3, 3)
            self.tokens.append(r.command_token)

        self.start_test_timestamp = -1

        # start the test
        self.device_app.run_test()
        self.test_ongoing = True

        # wait for test finished
        while self.test_ongoing == True:
            time.sleep(1)
        self.device_app.end_test()

        self.device_app.stop_status_thread()
        self.device_app.finalize()

        input("Press any key to exit\n")

    def _on_status_event(self, status_res):
        if self.test_ongoing:
            # in case of event notification, retrieve event data from device and clear events
            if status_res.m_isConditionEvent:
                res =  self.device_app.get_conditional_events()
                self.device_app.erase_conditional_events()
                if len(res.events) != 0:
                    print("Test started")

            token = status_res.m_executingCommandToken
            if token == 0:
                self.test_ongoing = False
                return
            # check if the status is correlated with temperature command
            for i in range(len(self.tokens)):
                if self.tokens[i] == token:
                    if i == 0 and self.start_test_timestamp < 0:
                        self.start_test_timestamp = status_res.m_temperatureBufferStartTime
                    buffer_timestamp = status_res.m_temperatureBufferStartTime - self.start_test_timestamp
                    print(f'Timestamp: {status_res.m_timestamp} | Target: {self.temperatures[i]} | First Temp. Timestamp: {buffer_timestamp}')

                    # print all temperatures in the status
                    for temp in status_res.m_heaterTemperature:
                        print(f'Timestamp: {buffer_timestamp} | Temperature: {round(temp, 3)}')
                        buffer_timestamp += 4
                    return





class Main():
        """
        The main run of the program
        It is made into a class in order to utilize event callbacks, a class
        is otherwise unnecessary
        """

        def __init__(self) -> None:
            self.device = TsaDevice(auto_connect_port=True) # Create device. It will establish a serial connection
            self.device.event_patient_response.connect(self._on_patient_response)
            self.response = ""
            self.test_ongoing = False
            self.temperatures = []
            self.temperature_file = open('test_temperatures.csv', mode='w')
            self.temperature_writer = csv.writer(self.temperature_file, delimiter=',', quotechar='"',
                                                 quoting=csv.QUOTE_MINIMAL)
            self.temperature_writer.writerow(['Timestamp', 'Temperature', 'Target'])

        def _on_patient_response(self, yes_press, no_press):
            if no_press:
                self.response = "n"
            elif yes_press:
                self.response = "y"

        def run(self):
            print("Connecting")
            self.device.start_status_thread(0.01)
            self.device.event_status_updated.connect(self._on_status_event)
	    self.device_app.set_TTL_output_duration(enums.TTLOUTChannel.TTLOUT, 20)
            print("Initializing and Self-Test")

            #self.device.enable_thermode(enums.ThermodeType.TSASlave)
            #self.device.set_active_thermode(enums.ThermodeType.TSASlave)
            #self.device.set_current_thermode(enums.DEVICE_TAG.Slave)
            self.device.enable_thermode(enums.ThermodeType.TSA)
            self.device.set_active_thermode(enums.ThermodeType.TSA)
            self.device.set_current_thermode(enums.DEVICE_TAG.Master)
            
            def check_condition():
                # Replace this condition with your own condition
                condition = True  # Example condition
                if condition:
                    messagebox.showinfo("Please remove the thermode from the patient's skin", "Condition is satisfied!")
                else:
                    messagebox.showwarning("Warning", "Condition is not satisfied!")
                root.destroy()
                # Create the main application window
            root = tk.Tk()
            root.title("Thermode is removed from patient's skin")

            # Button to check the condition
            check_button = tk.Button(root, text="OK, I have removed the thermode from the patient's skin", command=check_condition)
            check_button.pack(pady=20)
            root.mainloop()
            
            set_rest_mode_res = self.device.set_tcu_state(enums.SystemState.RestMode, run_self_test=True, wait_for_state=True)

            if set_rest_mode_res == None:
                print("Failed to send RestMode (SelfTest) request, exiting")
                self.device.finalize()
                return
            print("Self-Test finished")
            print("Going into TestInit mode")
            self.device.set_tcu_state(enums.SystemState.TestInit, run_self_test=False, wait_for_state=True)

            print("Running finite ramp test")
            print(f"State before finite_ramp = {self.device.status_state}")
            print(f"Temp before finite_ramp = {self.device.status_temp}")

            self.device.erase_conditional_events()

            print("Running finite ramp test - from current temp to 45 in 5sec, hold for 5sec, back to 32 in 5sec")
            self.tokens = []

            r=self.device.finite_ramp_by_temperature(45, 0.1, 0.1,
                                                     is_stop_on_response_unit_yes=False, time = 5000,
                                                     conditional_events_count=1)
            self.device.conditional_event(enums.EventCondition.TemperatureRaise, argument=44.0, ttl=1)
            self.tokens.append(r.command_token)
            self.temperatures.append(45)
            r=self.device.finite_ramp_by_time(45, time = 5000)
            self.tokens.append(r.command_token)
            self.temperatures.append(45)
            r=self.device.finite_ramp_by_temperature(32, 0.1, 0.1,
                                                     is_stop_on_response_unit_yes=False, time = 5000,
                                                     conditional_events_count=1)
            self.device.conditional_event(enums.EventCondition.TemperatureDrop, argument=40.0, ttl=1)
            self.temperatures.append(32)
            self.tokens.append(r.command_token)

            self.start_test_timestamp = -1
            print(f"State before run_test = {self.device.status_state}")
            print(f"Temp before run_test = {self.device.status_temp}")
            self.device.run_test()
            #time.sleep(5) #corresponds to the finite_ramp_by_temperature_section time. A while loop to wait for the temperature to be reached is also possible.
            # Wait for the tolerance
            #while self.device.status_temp <= 45 - 0.15:
            #    pass
            
            self.test_ongoing = True

            # wait for test finished
            while self.test_ongoing == True:
                time.sleep(1)
            self.device.end_test()

            self.device.stop_status_thread()
            self.device.finalize()

            input("Press any key to exit\n")

        def _on_status_event(self, status_res):
            if self.test_ongoing:
                # in case of event notification, retrieve event data from device and clear events
                if status_res.m_isConditionEvent:
                    res = self.device.get_conditional_events()
                    if res != None:
                        self.device.erase_conditional_events()
                        for ev in res.events:
                            if ev.condition == enums.EventCondition.TemperatureRaise:
                                print(f'Temperature raise {ev.peak_temp}')
                            elif ev.condition == enums.EventCondition.TemperatureDrop:
                                print(f'Temperature drop {ev.peak_temp}')
                            else:
                                print(f'Event {ev.condition}')


                token = status_res.m_executingCommandToken
                if token == 0:
                    self.test_ongoing = False
                    return
                # check if the status is correlated with temperature command
                for i in range(len(self.tokens)):
                    if self.tokens[i] == token:
                        if i == 0 and self.start_test_timestamp < 0:
                            self.start_test_timestamp = status_res.m_temperatureBufferStartTime
                        buffer_timestamp = status_res.m_temperatureBufferStartTime - self.start_test_timestamp
                        print(f'Timestamp: {status_res.m_timestamp} | Target: {self.temperatures[i]} | Token {token} | First Temp. Timestamp: {buffer_timestamp}')

                        # print all temperatures in the status
                        for temp in status_res.m_heaterTemperature:
                            self.temperature_writer.writerow(
                                [f'{buffer_timestamp}', f'{round(temp, 3)}', f'{self.temperatures[i]}'])

                            print(f'Timestamp: {buffer_timestamp} | Temperature: {round(temp, 3)}')
                            buffer_timestamp += 4
                        return



if __name__ == "__main__":
    __setup_logger(log_to_stdout=True, level=logging.ERROR)

    main = Main() #TestRamp()
    main.run()

