import enums
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)

class erase_conditional_events_command(command):
    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        # super(command, self).__init__()
        command.__init__(self, command_tag)
        # super()
        self.response = None
        self.command_id = enums.COMMAND_ID.EraseConditionalEvents

    def send_message(self):
        command.send_message(self)
        logger.info(f'\t{str(self)}')

    def __str__(self):
        return f'{command.__str__(self)}'
