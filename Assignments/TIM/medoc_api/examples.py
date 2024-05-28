from medoc_api.tsa_device import TsaDevice
import logging
import sys
import os
import enums
import tkinter as tk
from tkinter import messagebox
import time
import threading

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



class TestFeatures:
    """
    A test class that runs all features of TsaDevice to validate functionality
    """

    def __init__(self, cli_mode=False) -> None:
        self.device_app = TsaDevice(auto_connect_port=False) # Create device. It will establish a serial connection
        self.device_app.event_patient_response.connect(self._on_patient_response)
        self.device_app.event_status_updated.connect(self._on_status_update)
        self.response = ""
        self.cli_mode = cli_mode

    def _on_patient_response(self, yes_press, no_press):
        if yes_press:
            self.response = "y"
        elif no_press:
            self.response = "n"

    def _on_status_update(self, res):
        pass
    
    def wait_for_response(self):
        self.response = ""
        if self.cli_mode:
            self.response = get_patient_cli_response()
            return
        # In case of real patient response unit response will change by callback
        while self.response != "n" and self.response != "y":
            try:
                pass
            except KeyboardInterrupt:
                return

    def run(self):
        print("Version: ")
        print(self.device_app.get_version())
        self.device_app.start_status_thread(0.2)
        print("Enabling Main Thermode")
        self.device_app.enable_thermode(enums.ThermodeType.TSA)
        print("Enabling Slave Thermode")
        self.device_app.enable_thermode(enums.ThermodeType.TSASlave)
        print("Setting Slave to Active")
        self.device_app.set_active_thermode(enums.ThermodeType.TSASlave)
        print("Setting Slave as main thermode")
        self.device_app.set_current_thermode(enums.DEVICE_TAG.Slave)
        print("Main Thermode Active: ")
        print(self.device_app.get_active_thermode(enums.ThermodeType.TSA))
        print("Slave Thermode Active: ")
        print(self.device_app.get_active_thermode(enums.ThermodeType.TSASlave))
        print("Going into Rest Mode")
        print("Running Self-Test")

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
        print("Self-Test finished")
        print("Going into test Init Mode")
        self.device_app.set_tcu_state(enums.SystemState.TestInit, wait_for_state=True)
        print("Running finite ramp by temperature test")
        self.device_app.finite_ramp_by_temperature(45, 6, 6, is_stop_on_response_unit_yes=True)
        self.device_app.run_test()

        print("Waiting for temp to reach 45")
        while self.device_app.status_temp <= 45.0:
            pass
        
        print("Ending finite ramp by temperature test")
        self.device_app.end_test()
        print("Waiting for Patient response in order to continue")
        self.wait_for_response()
        print(f"Got response '{self.response}'")

        print("Going into TestInit mode")
        self.device_app.set_tcu_state(enums.SystemState.TestInit, wait_for_state=True)
        print("Running finite ramp by time test")
        self.device_app.finite_ramp_by_time(0.0, 10)
        self.device_app.run_test()

        print("Waiting for Patient response in order to continue")
        self.wait_for_response()
        self.device_app.end_test()

        # Wait for input and close status thread
        print("Test ended, press any key to exit")
        getch()
        self.device_app.stop_status_thread()

        # Call finalize to close the connection
        self.device_app.finalize()


class TestTemperature:
    """
    A test class that tests running programs via the API and logs program results to csv.
    
    It uses random values in range and tests going hot or cold to a temperature.
    """
    def __init__(self, append=False) -> None:
        """
        :param append: Whether to append to the csv file or to rewrite it fully.
        """
        self.target = 32.0
        self.test_ongoing = False
        self.temperature_file = None
        if not append or not os.path.isfile("test_temperatures.csv"):
            self.temperature_file = open('test_temperatures.csv', mode='w')
            self.temperature_writer = csv.writer(self.temperature_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.temperature_writer.writerow(['Timestamp', 'Temperature', 'Target'])
        else:
            self.temperature_file = open('test_temperatures.csv', mode='a')

    def run(self, num_tests=2):
        """
        Starts the test and finalizes at the end.
        
        :param num_tests: The number of times to run the procedure
        """

        print("Initializing")
        device_app = TsaDevice(auto_connect_port=False) # Create device. It will establish a serial connection
        device_app.start_status_thread(0.1)
        device_app.event_status_updated.connect(self._on_status_event)

        print("Beginning Self-Test")
        device_app.enable_thermode()
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
        
        device_app.set_tcu_state(enums.SystemState.RestMode, run_self_test=True, wait_for_state=True)
        device_app.set_tcu_state(enums.SystemState.TestInit, wait_for_state=True)
        print("Self-Test finished")
        messagebox.showinfo("Self-Test Complete", "Self-test has been completed.")
        self.test_ongoing = True

        for i in range(num_tests):
            rand_high = random.randrange(40, 50)
            rand_low = random.randrange(5, 15)

            device_app.finite_ramp_by_temperature(rand_high, 3, 3)
            self.target = rand_high
            device_app.run_test()

            while device_app.status_temp <= rand_high:
                pass

            device_app.stop_test()

            device_app.finite_ramp_by_temperature(rand_low, 3, 3)
            self.target = rand_low
            device_app.run_test()

            while device_app.status_temp >= rand_low:
                pass

            if i == num_tests - 1:
                device_app.end_test()
            else:
                device_app.stop_test()

        self.test_ongoing = False
        device_app.event_status_updated.erase(self._on_status_event)
        device_app.stop_status_thread()
        self.temperature_file.close()
        device_app.finalize()

        input("Press any key to exit\n")

    def _on_status_event(self, status_res):
        if self.test_ongoing:
            temperature_writer = csv.writer(self.temperature_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            temperature_writer.writerow([f'{status_res.m_timestamp}', f'{round(status_res.get_temp(), 3)}', f'{self.target}'])
            print(f'Timestamp: {status_res.m_timestamp} | Temperature: {round(status_res.get_temp(), 3)} | Target: {self.target}')


def get_patient_cli_response() -> str:
    """
    Prompt the user for a response and return it
    WARNING - This code will only run on Windows due to use of getch() from msvcrt library
    """
    print("Press `q` to continue, `y` for Yes or `n` for No")
    res = ''
    while res not in [ 'q', 'y', 'n' ]:
        res = getch()
        print()

    return res

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

        def _on_patient_response(self, yes_press, no_press):
            if no_press:
                self.response = "n"
            elif yes_press:
                self.response = "y"

        def run(self):
            print("Connecting")
            self.device.start_status_thread(0.1)

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
            root = tk.Tk()
            root.title("Self test complete")
            messagebox.showinfo("Self-Test Complete", "You can now attach the thermode to the patient.")
            root.destroy()
            print("Going into TestInit mode")
            self.device.set_tcu_state(enums.SystemState.TestInit, run_self_test=False, wait_for_state=True)

            print("Running finite ramp test")
            print(f"State before finite_ramp = {self.device.status_state}")
            print(f"Temp before finite_ramp = {self.device.status_temp}")
            
            print("Running finite ramp test - from current temp to 45 in 5sec, hold for 5sec, back to 32 in 5sec")
            self.device.finite_ramp_by_temperature(45, 0.1, 0.1, is_stop_on_response_unit_yes=False, time = 5000)
            print(f"State before run_test = {self.device.status_state}")
            print(f"Temp before run_test = {self.device.status_temp}")
            self.device.run_test()
            time.sleep(5) #corresponds to the finite_ramp_by_temperature_section time. A while loop to wait for the temperature to be reached is also possible.
            # Wait for the tolerance
            #while self.device.status_temp <= 45 - 0.15:
            #    pass
            self.device.stop_test() 
            self.device.finite_ramp_by_temperature(45, 0.1, 0.1, is_stop_on_response_unit_yes=False, time=5000)
            print(f"State before run_test = {self.device.status_state}")
            print(f"Temp before run_test = {self.device.status_temp}")
            self.device.run_test()
            time.sleep(5)
            self.device.stop_test()
            self.device.finite_ramp_by_temperature(32, 0.1, 0.1, is_stop_on_response_unit_yes=False, time=10000)
            print(f"State before run_test = {self.device.status_state}")
            print(f"Temp before run_test = {self.device.status_temp}")
            self.device.run_test()
            time.sleep(10)
            self.device.stop_test()
            start_time = time.time()
            # Create and start the thread for checking key press
            keypress_thread = threading.Thread(target=check_key_press)
            keypress_thread.start()
            while time.time() < start_time + 600:
                #insert your condition to get out of idle. This is for keeping serial connection open. Currently set to 10min hold at 32 and refreshes every 10sec
                #else:
                self.device.finite_ramp_by_temperature(32, 0.1, 0.1, is_stop_on_response_unit_yes=False, time=10000)
                self.device.run_test()
                print("Holding serial connection open")
                time.sleep(10)
                self.device.stop_test()
            #self.device.end_test()
            

            # Wait for event caused by patient response unit
            # self.response = ""
            # while self.response != "n":
            #     try:
            #         pass
            #     except KeyboardInterrupt:
            #         break

            # Simulate patient response via cli
            #self.response = get_patient_cli_response()
            #if self.response == "y":
            #    self.device.simulate_response_unit(True, False)
            #elif self.response == "n":
            #    self.device.simulate_response_unit(False, True)

            #print(f"Got response {self.response}")

            self.device.end_test()

            # Wait for input and close status thread
            print("Test ended, press any key to exit")
            getch()
            self.device.stop_status_thread()

            # Call finalize to close the connection
            self.device.finalize()

if __name__ == "__main__":
    __setup_logger(log_to_stdout=True, level=logging.ERROR)

    main = Main()
    main.run()

