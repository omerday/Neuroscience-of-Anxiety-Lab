import logging
from medoc_api.commands.m_message import message

logger = logging.getLogger(__name__)


class response(message):
    def __init__(self, command_id=None):
        message.__init__(self)
        self.command_ack_code = None

    def read_data(self, buffer, start_position=0):
        """
        read data from byte array to self
        :return:
        """
        pass

    def __str__(self):
        base = message.__str__(self)
        return f'{base} ack code {str(self.command_ack_code)}:::'

    def response_message(self):
        """
        create response message
        :return:
        """
        logger.info(f'RESPONSE::: {str(self)}\n')
