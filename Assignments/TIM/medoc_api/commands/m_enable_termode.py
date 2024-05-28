from medoc_api import enums
from medoc_api.commands import m_command, m_message
import logging

from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


class enable_termode_command(command):
    def __init__(self):
        command.__init__(self)
        self.response = None
        self.m_isEnabled = True
        self.m_thermodeType = enums.ThermodeType.TSA
        self.command_id = enums.COMMAND_ID.EnableThermode

    def build_command(self, data):
        """
        build parameters from json file
        :param data: instance of command from json file from him parameters
        :return:
        """
        if 'm_isEnabled' in data.keys():
            self.m_isEnabled = data['m_isEnabled']
        if 'm_thermodeType' in data.keys():
            self.m_thermodeType = enums.ThermodeType(data['m_thermodeType'])

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00] * 2
        extra_data[0] = self.m_thermodeType.value
        extra_data[1] = 1 if self.m_isEnabled else 0
        return extra_data

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}'
