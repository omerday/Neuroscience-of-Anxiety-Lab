from medoc_api import enums
from medoc_api.commands import m_command, m_message
import logging

from medoc_api.commands.m_command import command

logger = logging.getLogger(__name__)


# TODO Need Testing
class stop_test_command(command):
    def __init__(self):
        command.__init__(self)
        self.response = None
        self.command_id = enums.COMMAND_ID.StopTest

    def write_data(self):
        command.write_data(self)

        return []

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t\n{command.__str__(self)}'
