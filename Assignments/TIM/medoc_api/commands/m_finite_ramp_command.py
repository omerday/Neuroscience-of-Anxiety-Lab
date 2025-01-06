from medoc_api.commands.m_temperature_command import *
import medoc_api.enums as enums


class finite_ramp_command(temperature_command):
    STOP_ON_YES_BIT = 0
    STOP_ON_NO_BIT = 1

    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        # super(command, self).__init__()
        temperature_command.__init__(self, command_tag)
        self.m_temperature = 0
        self.m_time = 0
        self.m_isPeakDetect = False
        self.m_isCreateTimeMark = False
        self.m_isDynamicFactor = False
        self.m_isStopOnResponseUnitYes = None
        self.m_isStopOnResponseUnitNo = None

