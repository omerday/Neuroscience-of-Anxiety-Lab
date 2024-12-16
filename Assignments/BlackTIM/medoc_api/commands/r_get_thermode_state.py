from medoc_api.Utilities import converters
from medoc_api.commands.m_message import message
from medoc_api.commands.response import response
import logging

logger = logging.getLogger(__name__)


class get_thermode_state_response(response):
    def __init__(self):
        response.__init__(self)
        self.m_version = None

    def read_data(self, buffer, start_position=0):
        count = response.read_data(buffer, start_position)
        self.m_version = converters.to_string(buffer, start_position)

    def response_message(self):
        logger.info(f'{str(self)}')

    def __str__(self):
        base = message.__str__(self)
        return f'RESPONSE::: {message.__str__(self)} ack code {str(self.command_ack_code)} \n\t\t\t\t\t\t\t ' \
               f'GetVersion: {self.m_version}\n '