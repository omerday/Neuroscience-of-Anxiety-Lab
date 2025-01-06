import medoc_api.enums as enums
from medoc_api.commands import m_command, m_message
import logging

from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


class end_test_command(command):
    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        command.__init__(self, command_tag)
        self.response = None
        self.command_id = enums.COMMAND_ID.EndTest


    def write_data(self):
        command.write_data(self)

        return []

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t\n{command.__str__(self)}'




