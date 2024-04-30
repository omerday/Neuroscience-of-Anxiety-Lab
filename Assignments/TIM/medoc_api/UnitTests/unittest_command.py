import unittest

from medoc_api import enums
from medoc_api.commands import m_getVersion_command, m_message, m_set_TCU_state
from medoc_api.commands.m_clear_command_buffer import clear_command_buffer_command
from medoc_api.commands.m_end_test_command import end_test_command
from medoc_api.commands.m_finite_ramp_by_temperature_command import finite_ramp_by_temperature_command
from medoc_api.commands.m_finite_ramp_by_time_command import finite_ramp_by_time_command
from medoc_api.commands.m_getstatusTCU_command import get_status_TCU_command
from medoc_api.commands.m_run_test import run_test_command
from medoc_api.commands.m_simulate_response_unit import simulate_unit_response_command
from medoc_api.commands.m_stop_test_command import stop_test_command


class commands_TestCase(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def setUp(self):
        self.get_version_buffer = [73, 0, 8, 37, 0, 0, 0, 1, 0]
        self.token = 1
        self.set_TCU_command_buffer = [0xc0, 0x0, 0xa, 0x29, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0]
        # команды с завершающим нулем
        # m_state = SystemState.RestMode
        # m_runSelfTest = True
        # m_token = 0x5c1
        # m_tag = 0
        # m_id = 0x29
        self.check_set_tcu_state_rest_mode = [0xAA, 0x0, 0xA, 0x29, 0x0, 0x0, 0x5, 0xC1, 0x0, 0x2, 0x1, 0x0]

        # m_token = 0x9FA
        # m_tag = 0
        # m_id = 0x29
        self.check_clear_buffer = [0xEC, 0x0, 0x8, 0x1B, 0x0, 0x0, 0x9, 0xFA, 0x0]

        # run test command
        # resetclock = True
        # m_token = 0xA00
        # m_tag = 0
        # m_id = 0x16
        self.check_run_test = [0xF, 0x0, 0x9, 0x16, 0x0, 0x0, 0xA, 0x0, 0x0, 0x1, 0x0]

        # finiterampbytime command
        # AllowSafeDurationOffset = NULL

        # cmdtime = 0x64
        # m_token = 4565
        # AllowSafeDurationOffset = null
        # Temperature = 32
        # Time = 0x64
        # conditioneventcount = 0
        # conditioneventlength = 0
        # iswaitfortrigger = False
        # ispeakdetect = False
        # iscreatetimemark = False
        # UseTimeMark = False
        # usedynamicfactor = False
        # isAllowEmptyBuffer = True
        # IgnoreKdPidParameter = False
        # IsStopOnResponseUnitYes = False
        # IsStopOnResponseUnitNo = False
        # m_tag = 0
        # m_id = 28
        self.finite_ramp_by_time = [0xCB, 0x0, 0x11, 0x1C, 0x0, 0x0, 0x11, 0xD5, 0x0, 0xC, 0x80, 0x0, 0x0, 0x0, 0x64,
                                    0x80, 0x0, 0x0, 0x0]

        """
            stop test command
            m_token = 3175
            m_tag = 0
            
        """
        self.stop_test = [0x25, 0x0, 0x8, 0x2f, 0x0, 0x0, 0xc, 0x67, 0x0]

        # m_token = 8868
        # Temperature = 34
        # Time = 154
        # lowmargin = 0.10000000000000001
        # highlimit = 0.20000000000000001
        # m_tag = 0
        # m_id = 28
        self.finite_ramp_by_temperature = [0xBC, 0x0, 0x15, 0x1D, 0x0, 0x0, 0x22, 0xA4, 0x0, 0xD, 0x48, 0x0, 0xA, 0x0,
                                           0x14, 0x0, 0x0, 0x0, 0x9A, 0xA0, 0x0, 0x0, 0x0]

        """
            end test command
            m_token = 3175
            m_tag = 0

        """
        self.end_test = [0x68, 0x0, 0x8, 0x19, 0x0, 0x0, 0xD, 0xE8, 0x0]

        """
            simulate_unit_response command
            m_token = 18569
            m_tag = 0
            IsYesPressed = False
            IsNoPressed = False
        """
        self.simulate_unit_response = [0x70, 0x0, 0x9, 0x2D, 0x0, 0x0, 0x48, 0x89, 0x0, 0x0, 0x0]

        """
                    getStatusTCU command
                    m_token = 18571
                    m_tag = 0
                """
        self.get_status_TCU = [0xE, 0x0, 0x8, 0x21, 0x0, 0x0, 0x48, 0x8B, 0x0]

    def test_check_create_get_version_command_return_valid_command(self):
        com = m_getVersion_command.getVersion_command()

        com.command_token = self.token
        com.command_id = enums.COMMAND_ID["GetVersion"]
        com.to_bytes()
        self.assertEqual(self.get_version_buffer, com.command_array)

    # def test_check_create_set_TCU_state_command_return_valid_command(self):
    #     com = m_set_TCU_state.set_TCU_state_command()
    #
    #     com.command_token = self.token
    #     com.command_id = m_message.COMMAND_ID["SetTcuState"]
    #     com.to_bytes()
    #     self.assertEqual(self.set_TCU_command_buffer, com.command_array)

    def test_check_create_set_TCU_state_RestMode_command_return_valid_command(self):
        com = m_set_TCU_state.set_TCU_state_command()

        com.command_token = 0x5c1
        com.command_id = enums.COMMAND_ID["SetTcuState"]
        com.m_state = enums.SystemState["RestMode"]

        com.to_bytes()
        self.assertEqual(self.check_set_tcu_state_rest_mode, com.command_array)

    def test_check_create_clear_command_buffer_command_return_valid_command(self):
        com = clear_command_buffer_command()

        com.command_token = 0x9FA
        com.command_id = enums.COMMAND_ID["ClearCommandBuffer"]
        com.to_bytes()
        self.assertEqual(self.check_clear_buffer, com.command_array)

    def test_check_run_test_command_command_return_valid_command(self):
        com = run_test_command()

        com.command_token = 0xA00
        com.command_id = enums.COMMAND_ID["RunTest"]
        com.m_isResetClock = True
        com.to_bytes()
        self.assertEqual(self.check_run_test, com.command_array)

    def test_check_finite_ramp_by_time_command_return_valid_command(self):
        com = finite_ramp_by_time_command()

        com.command_token = 4565
        com.command_id = enums.COMMAND_ID["FiniteRampByTime"]
        com.m_temperature = 32
        com.m_time = 100
        com.m_isWaitForTrigger = False
        com.m_isPeakDetect = False
        com.m_isCreateTimeMark = False
        com.m_isUseTimeMark = False
        com.m_isDynamicFactor = False
        com.m_isAllowEmptyBuffer = True
        com.m_isIgnoreKdPidParameter = False
        com.m_allowSafeDurationOffset = None
        com.m_isStopOnResponseUnitYes = False
        com.m_isStopOnResponseUnitNo = False

        com.to_bytes()
        self.assertEqual(self.finite_ramp_by_time, com.command_array)

    def test_stop_test_command_return_valid_command(self):
        com = stop_test_command()

        com.command_token = 3175
        com.command_id = enums.COMMAND_ID["StopTest"]
        com.to_bytes()
        self.assertEqual(self.stop_test, com.command_array)

    def test_check_finite_ramp_by_temperature_command_return_valid_command(self):
        com = finite_ramp_by_temperature_command()

        com.command_token = 8868
        com.command_id = enums.COMMAND_ID["FiniteRampByTemperature"]
        com.m_temperature = 34
        com.m_time = 154
        com.m_isWaitForTrigger = False
        com.m_isPeakDetect = False
        com.m_isCreateTimeMark = False
        com.m_isDynamicFactor = False
        com.m_isAllowEmptyBuffer = True
        com.m_ignoreKdPidParameter = True
        com.m_allowSafeDurationOffset = None
        com.m_lowMargin = 0.10000000000000001
        com.m_highMargin = 0.20000000000000001

        com.to_bytes()
        self.assertEqual(self.finite_ramp_by_temperature, com.command_array)

    def test_end_test_command_return_valid_command(self):
        com = end_test_command()

        com.command_token = 3560
        com.command_id = enums.COMMAND_ID["EndTest"]
        com.to_bytes()

        self.assertEqual(self.end_test, com.command_array)

    def test_simulate_unit_response_command_return_valid_command(self):
        com = simulate_unit_response_command()

        com.command_token = 18569
        com.command_id = enums.COMMAND_ID["SimulateResponseUnit"]
        com.m_isYesPressed = False
        com.m_isNoPressed = False
        com.to_bytes()

        self.assertEqual(self.simulate_unit_response, com.command_array)

    def test_get_status_tcu_command_return_valid_command(self):
        com = get_status_TCU_command()

        com.command_token = 18571
        com.command_id = enums.COMMAND_ID["GetStatusTCU"]
        com.to_bytes()

        self.assertEqual(self.get_status_TCU, com.command_array)
