from medoc_api import enums
import logging
from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


class get_errors_command(command):
    def __init__(self):
        command.__init__(self)
        self.response = None
        self.is_generated = True
        self.command_id = enums.COMMAND_ID.GetErrors

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00]
        extra_data[0] = 0x1 if self.is_generated else 0x0

        return extra_data

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}'
