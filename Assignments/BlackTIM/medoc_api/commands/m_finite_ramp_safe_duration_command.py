from medoc_api.commands.m_finite_ramp_command import *


class finite_ramp_safe_duration_command(finite_ramp_command):
    def __init__(self):
        # super(command, self).__init__()
        finite_ramp_command.__init__(self)

        self.m_allowSafeDurationOffset = None
