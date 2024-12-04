from medoc_api import enums
import logging
from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


class erase_error_command(command):
    def __init__(self):
        command.__init__(self)
        self.command_id = enums.COMMAND_ID.EraseErrors

    def write_data(self):
        return command.write_data(self)

    def send_message(self):
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}'
