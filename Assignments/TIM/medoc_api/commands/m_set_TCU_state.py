import enums
from commands import m_command, m_message
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)


class set_TCU_state_command(command):
    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        command.__init__(self, command_tag)
        self.m_state = enums.SystemState.SafeMode
        self.m_runSelfTest = True
        self.response = None
        self.command_id = enums.COMMAND_ID.SetTcuState

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00] * 2
        extra_data[0] = self.m_state.value
        extra_data[1] = 1 if self.m_runSelfTest else 0

        return extra_data

    def build_command(self, data):
        """
        build parameters from json file
        :param data: instance of command from json file from him parameters
        :return:
        """
        if 'm_state' in data.keys():
            self.m_state = enums.SystemState(data['m_state'])
        if 'm_runSelfTest' in data.keys():
            self.m_runSelfTest = data['m_runSelfTest']

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}\nPARAMETERS\t\t\t\t\t\tm_runSelfTest = {self.m_runSelfTest}\n\t\t\t\t\t\t\t' \
               f'\tm_state = {str(self.m_state)}'
