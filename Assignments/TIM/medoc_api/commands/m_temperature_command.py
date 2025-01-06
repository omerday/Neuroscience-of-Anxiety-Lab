from medoc_api.commands.m_command import command
import medoc_api.enums as enums


class temperature_command(command):
    MAX_EVENTS_NO = 255
    WAIT_TRIGGER_BIT = 0
    PEAK_DETECT_BIT = 1
    CREATE_TIME_MARK_BIT = 2
    USE_UNLIMITED_SETPOINT_BIT = 4
    IGNORE_KD_PID_PARAMETER_BIT = 5
    USE_DYNAMIC_FACTOR = 6
    ALLOW_EMPTY_BUFFER_BIT = 7
    ALLOW_SAFE_DURATION_OFFSET = 3

    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        command.__init__(self, command_tag)
        #from temperuture command
        self.m_isWaitForTrigger = False
        self.m_isAllowEmptyBuffer = True
        self.m_ignoreKdPidParameter = False
        self.m_condEventsNo = 0
        self.m_conditionEventsLength = 0

        # from FiniteRampCommand
