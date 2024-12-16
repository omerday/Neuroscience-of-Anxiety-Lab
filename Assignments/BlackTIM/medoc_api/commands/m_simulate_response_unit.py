from medoc_api import enums
from medoc_api.Utilities import converters
from medoc_api.commands import m_command, m_message
import logging

from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


class simulate_unit_response_command(command):
    BIT_YES = 0
    BIT_NO = 1

    def __init__(self):
        command.__init__(self)
        self.response = None
        self.m_isYesPressed = False
        self.m_isNoPressed = False
        self.command_id = enums.COMMAND_ID.SimulateResponseUnit

    def build_command(self, data):
        """
        build parameters from json file
        :param data: instance of command from json file from him parameters
        :return:
        """
        if 'm_isYesPressed' in data.keys():
            self.m_isYesPressed = data['m_isYesPressed']
        if 'm_isNoPressed' in data.keys():
            self.m_isNoPressed = data['m_isNoPressed']

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00]
        options_byte = 0

        options_byte = converters.set_bit(options_byte, self.BIT_YES, self.m_isYesPressed)
        options_byte = converters.set_bit(options_byte, self.BIT_NO, self.m_isNoPressed)
        extra_data[0] = options_byte

        return extra_data

    # Path: commands\m_run_test.py
    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t\n{command.__str__(self)}'
