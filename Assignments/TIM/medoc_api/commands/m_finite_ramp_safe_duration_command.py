from medoc_api.commands.m_finite_ramp_command import *
import medoc_api.enums as enums


class finite_ramp_safe_duration_command(finite_ramp_command):
    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        # super(command, self).__init__()
        finite_ramp_command.__init__(self, command_tag)

        self.m_allowSafeDurationOffset = None
