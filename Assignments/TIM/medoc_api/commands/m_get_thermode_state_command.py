import medoc_api.enums as enums
from medoc_api.commands import m_command, m_message
import logging

from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


class get_thermode_state_command(command):
    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        # super(command, self).__init__()
        command.__init__(self, command_tag)
        self.response = None
        self.command_id = enums.COMMAND_ID.GetThermodeState

    def send_message(self):
        # command.send_message(self)
        logger.info(f'\t{str(self)}')

    def __str__(self):
        return f'{command.__str__(self)}'
