import medoc_api.enums as enums
from medoc_api.commands import m_command, m_message
import logging

from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


class run_test_command(command):
    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        command.__init__(self, command_tag)
        self.response = None
        self.m_isResetClock = True
        self.command_id = enums.COMMAND_ID.RunTest

    def build_command(self, data):
        """
        build parameters from json file
        :param data: instance of command from json file from him parameters
        :return:
        """
        if 'm_isResetClock' in data.keys():
            self.m_isResetClock = data['m_isResetClock']

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00]
        extra_data[0] = 0x1 if self.m_isResetClock else 0x0

        return extra_data

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}\nPARAMETERS:\t\t\t\t\t\t Reset clock: {self.m_isResetClock}'
