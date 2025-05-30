from medoc_api import enums
import logging
from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


class clear_command_buffer_command(command):
    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        command.__init__(self, command_tag)
        self.response = None
        self.command_id = enums.COMMAND_ID.ClearCommandBuffer

    def write_data(self):
        return command.write_data(self)

    def send_message(self):
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}'
