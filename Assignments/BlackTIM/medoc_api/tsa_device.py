import time
import sys
import logging
import threading

from medoc_api.token_holder import TokenHolder
from medoc_api.command_api import CommandAPI
from medoc_api.event import Event
from medoc_api.event import TypedEvent

from medoc_api.c_api import CApi

from medoc_api.connector import connector
from medoc_api.commands.response import response
from medoc_api import enums


########################## Command imports #######################################
from medoc_api.commands.m_getVersion_command import getVersion_command
from medoc_api.commands.m_getstatusTCU_command import get_status_TCU_command
from medoc_api.commands.m_set_TCU_state import set_TCU_state_command
from medoc_api.commands.m_clear_command_buffer import clear_command_buffer_command
from medoc_api.commands.m_enable_termode import enable_termode_command
from medoc_api.commands.m_end_test_command import end_test_command
from medoc_api.commands.m_finite_ramp_by_temperature_command import finite_ramp_by_temperature_command
from medoc_api.commands.m_finite_ramp_by_time_command import finite_ramp_by_time_command
from medoc_api.commands.m_get_active_thermode import get_active_thermode_command
from medoc_api.commands.m_set_active_thermode import set_active_thermode_command
from medoc_api.commands.m_run_test import run_test_command
from medoc_api.commands.m_simulate_response_unit import simulate_unit_response_command
from medoc_api.commands.m_stop_test_command import stop_test_command
##################################################################################

class TsaDevice:
    """
    Class to communicate with a Medoc TSA based Device
    
    It contains wrappers for sending commands through functions
    It also contains threads for receiving status updates on a timely basis, and for receiving
    events from a patient response device.
    """

    def __init__(self, auto_connect_port=True, preferences_path="./medoc_api/preferences.json") -> None:
        self.current_thermode: enums.DEVICE_TAG = enums.DEVICE_TAG.Master
        self.token_holder: TokenHolder = TokenHolder()

        if auto_connect_port and sys.platform != "win32" and not "linux" in sys.platform:
            logging.getLogger().error("`auto_connect_port` is only available on Windows or Linux, please set port in `preferences.json`")
            auto_connect_port = False

        self.connector: connector = connector(
            path_to_prefernces=preferences_path,
            auto_detect=auto_connect_port,
            token_holder=self.token_holder
            )

        self.event_status_updated: Event = Event()
        self.event_patient_response: TypedEvent = TypedEvent(bool, bool)

        self.busy: bool = False
        self.last_safety_level = 0.0
        self.safety_start_time = time.time() # The time since safety was switched

        self.status_state = None
        self.status_temp = 0.0

        self.status_thread = None
        self.status_thread_stop = False

        self.event_status_updated.connect(self._on_get_status_event)

    @staticmethod
    def validate_response(res: response):
        """
        Return the response if valid or `None` if invalid
        """
        return res if \
            (res is not None and res.command_ack_code == enums.ACKCODE.Ok) \
                else None

    @staticmethod
    def get_safety_ms(temp: float):
        """
        Get the maximum time in miliseconds that a temperature is allowed to be upheld
        """
        return CApi.get_safety_ms(temp)

    @staticmethod
    def get_safety_level(temp: float):
        """
        Get the temperature threshold for temp
        """
        return CApi.get_safety_level(temp)

    def _on_get_status_event(self, status_res):
        self.status_state = enums.SystemState(status_res.get_state())
        self.status_temp = status_res.get_temp()

        safety_level = TsaDevice.get_safety_level(self.status_temp) 
        if safety_level != self.last_safety_level:
            self.last_safety_level = safety_level
            self.safety_start_time = time.time()
        
        safety_ms = TsaDevice.get_safety_ms(self.status_temp)
        if time.time() >= self.safety_start_time + (safety_ms / 1000):
            self._safety_failure()
        
        # message = f"Timestamp:{status_res.m_timestamp} | Temperature: {self.status_temp} | State: {self.status_state}\n"
        # print(message)
        # logging.getLogger().info(message)

        yes_press = status_res.m_isResponseUnitYesOn 
        no_press = status_res.m_isResponseUnitNoOn
        if no_press or yes_press:
            self.event_patient_response.emit(yes_press, no_press)

    def _safety_failure(self):
        """
        Method to call when a safety failure has occured in order to shut down the program
        """
        self.end_test()
        self.stop_status_thread()
        self.finalize()
        logging.getLogger().error("TEMPERATURE SAFETY FAILURE - TEMPERATURE REACHED %f", self.status_temp)
        raise RuntimeError(f"TEMPERATURE SAFETY FAILURE - TEMPERATURE REACHED {self.status_temp}")

    def start_status_thread(self, update_rate=1.0):
        """
        Start the running of the status update
        """
        self.status_thread = threading.Thread(target=self._status_thread, args=[update_rate])
        self.status_thread.start()
        self.status_thread_stop = False

    def stop_status_thread(self):
        """
        Stop the status thread
        """
        self.status_thread_stop = True

    def send_command(self, com, data=None):
        """
        Send a command to the device. If blocking is a problem, check the `busy` variable before calling.

        :param com: The command object to be sent
        """
        while self.busy:
            pass

        self.busy = True
        res = CommandAPI.send_command_immediate(
            self.connector.tunnel,
            self.token_holder,
            com,
            data,
            inc_token=True
            )

        self.busy = False
        return res

    def set_current_thermode(self, thermode_type: enums.DEVICE_TAG):
        self.current_thermode = thermode_type

    def get_current_thermode(self) -> enums.DEVICE_TAG:
        return self.current_thermode

    def finalize(self):
        """
        Close all components and threads and prepare for exit
        """
        while self.busy:
            pass

        self.stop_status_thread()
        self.connector.finalize()

    def set_temperature(self, temp, low_margain, high_margain):
        """
        Set the temperature manually to desired value.
        """
        if self.status_state != enums.SystemState.TestInit:
            self.set_tcu_state(enums.SystemState.TestInit, wait_for_state=True)

        heat = self.status_temp <= temp

        self.finite_ramp_by_temperature(temp, low_margain, high_margain)
        self.run_test()

        if heat:
            while self.status_temp <= temp:
                pass
        else:
            while self.status_temp >= temp:
                pass

        self.end_test()

    def get_version(self):
        data = {
            "name": "GetVersion",
            "commandId": 37
        }

        com = getVersion_command()
        res = self.send_command(com, data)
        return self.validate_response(res)

    def get_status(self):
        data = {
            "name": "GetStatusTCU",
            "commandId": 33
        }

        com = get_status_TCU_command()
        res = self.send_command(com, data)
        return self.validate_response(res)

    def enable_thermode(self, thermode_type: enums.ThermodeType=enums.ThermodeType.TSA):
        data = {
            "name": "EnableTermode",
            "commandId": 83,
            "m_thermodeType": thermode_type,
            "m_isEnabled": True
        }

        com = enable_termode_command()
        res = self.send_command(com, data)
        return self.validate_response(res)

    def disable_thermode(self, thermode_type: enums.ThermodeType=enums.ThermodeType.TSA):
        data = {
            "name": "EnableTermode",
            "commandId": 83,
            "m_thermodeType": thermode_type,
            "m_isEnabled": False
        }

        com = enable_termode_command()
        res = self.send_command(com, data)
        return self.validate_response(res)

    def set_tcu_state(self, state: enums.SystemState, run_self_test=True, wait_for_state=False, wait_timeout=30.0):
        data = {
            "name": "SetTcuState",
            "commandId": 41,
            "m_state": state,
            "m_runSelfTest": run_self_test
        }

        if wait_for_state and self.status_thread_stop:
            raise ValueError("wait_for_state must be used with status thread running")

        start_time = time.time()
        com = set_TCU_state_command()
        res = self.send_command(com, data)
        valid = self.validate_response(res)

        if valid and wait_for_state:
            while self.status_state != state and time.time() <= (start_time + wait_timeout):
                pass
        
        time.sleep(0.5)

        return valid

    def get_active_thermode(self, thermode_id=enums.ThermodeType.TSA):
        if isinstance(thermode_id, enums.ThermodeType):
            thermode_id = thermode_id.value
        data = {
            "name": "GetActiveThermode",
            "commandId": 19,
            "m_thermodeId": thermode_id
        }

        com = get_active_thermode_command()
        res = self.send_command(com, data)
        return self.validate_response(res)

    def set_active_thermode(self, thermode_id=enums.ThermodeType.TSA):
        if isinstance(thermode_id, enums.ThermodeType):
            thermode_id = thermode_id.value
        data = {
            "name": "SetActiveThermode",
            "commandId": 18,
            "m_thermodeId": thermode_id
        }

        com = set_active_thermode_command()
        res = self.send_command(com, data)
        return self.validate_response(res)


    def clear_command_buffer(self):
        data = {
            "name": "ClearCommandBuffer",
            "commandId": 27
        }

        com = clear_command_buffer_command()
        res = self.send_command(com, data)
        return self.validate_response(res)

    def run_test(self, is_reset_clock=False):
        data = {
            "name": "RunTest",
            "commandId": 22,
            "m_isResetClock": is_reset_clock
        }
        
        com = run_test_command()
        res = self.send_command(com, data)
        return self.validate_response(res)

    def finite_ramp_by_temperature(self,
                                    temperature,
                                    low_margain,
                                    high_margain,
                                    allow_safe_duration_offset=False, 
                                    is_wait_for_trigger=False, 
                                    is_peak_detect=False, 
                                    is_create_time_mark=False,
                                    is_dynamic_factor=False,
                                    is_allow_empty_buffer=True,
                                    ignore_kd_pid_parameter=False,
                                    is_stop_on_response_unit_no=False,
                                    is_stop_on_response_unit_yes=False,
                                    time=100
                                    ):
        data = {
            "name": "FiniteRampByTemperature",
            "commandId": 29,
            "m_allowSafeDurationOffset": allow_safe_duration_offset,
            "m_isWaitForTrigger": is_wait_for_trigger,
            "m_isPeakDetect": is_peak_detect,
            "m_isCreateTimeMark": is_create_time_mark,
            'm_isDynamicFactor': is_dynamic_factor,
            'm_isAllowEmptyBuffer': is_allow_empty_buffer,
            'm_ignoreKdPidParameter': ignore_kd_pid_parameter,
            'm_isStopOnResponseUnitNo': is_stop_on_response_unit_no,
            'm_isStopOnResponseUnitYes': is_stop_on_response_unit_yes,
            'm_temperature': temperature,
            'm_time': time
        }

        com = finite_ramp_by_temperature_command()
        com.m_lowMargin = low_margain
        com.m_highMargin = high_margain
        res = self.send_command(com, data=data)
        return self.validate_response(res)

    def stop_test(self):
        data = {
            "name": "StopTest",
            "commandId": 47
        }
        
        com = stop_test_command()
        res = self.send_command(com, data=data)
        return self.validate_response(res)

    def finite_ramp_by_time(self, 
                                    temperature: float,
                                    time: int,
                                    allow_safe_duration_offset=False, 
                                    is_wait_for_trigger=False, 
                                    is_peak_detect=False,
                                    is_create_time_mark=False,
                                    is_use_time_mark=False,
                                    is_dynamic_factor=False,
                                    is_allow_empty_buffer=True,
                                    ignore_kd_pid_parameter=False,
                                    is_stop_on_response_unit_no=False,
                                    is_stop_on_response_unit_yes=False,
                                    ):
        """
        Request the Finite Ramp By Time test
        @param temperature: The target temperature
        @param time: The amount of time to reach the temperature
        @param is_stop_on_response_unit_no: Will the test end when the patient presses the "N" button on the response unit
        @param is_stop_on_response_unit_yes: Will the test end when the patient presses the "Y" button on the response unit
        """
        data = {
				"commandId": 28,
				"name": "FiniteRampByTime",
				"m_allowSafeDurationOffset": allow_safe_duration_offset,
				"m_isWaitForTrigger": is_wait_for_trigger,
				"m_isPeakDetect": is_peak_detect,
				"m_isCreateTimeMark": is_create_time_mark,
				"m_isUseTimeMark": is_use_time_mark,
				"m_isDynamicFactor": is_dynamic_factor,
				"m_isAllowEmptyBuffer": is_allow_empty_buffer,
				"m_ignoreKdPidParameter": ignore_kd_pid_parameter,
				"m_isStopOnResponseUnitNo": is_stop_on_response_unit_no,
				"m_isStopOnResponseUnitYes": is_stop_on_response_unit_yes,
				"m_temperature": temperature,
				"m_time": time
        }

        com = finite_ramp_by_time_command()
        res = self.send_command(com, data=data)
        return self.validate_response(res)

    def end_test(self):
        data = {
            "name": "EndTest",
            "commandId": 25
        }

        com = end_test_command()
        res = self.send_command(com, data=data)
        return self.validate_response(res)

    def simulate_response_unit(self, is_yes_pressed, is_no_pressed):
        data = {
            "name": "SimulateResponseUnit",
            "commandId": 45,
            "m_isYesPressed": is_yes_pressed,
            "m_isNoPressed": is_no_pressed
        }

        com = simulate_unit_response_command()
        res = self.send_command(com, data=data)
        return self.validate_response(res)

    def _status_thread(self, update_rate):
        while not self.status_thread_stop:
            while self.busy:
                pass

            res = self.get_status()
            if res:
                self.event_status_updated.emit(res)
            time.sleep(update_rate)

