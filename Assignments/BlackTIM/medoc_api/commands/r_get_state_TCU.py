from medoc_api.commands.response import response
import logging

logger = logging.getLogger(__name__)


class get_stateTCU_response(response):
    def __init__(self):
        response.__init__(self)
        self.m_state = None
        self.m_runSelfTest = None

    def read_data(self, buffer, start_position=0):
        pass

    def response_message(self):
        logger.info(f'{str(self)}')

    def __str__(self):
        base = str(response.__str__(self))

        return f"{0} SYSTEMSTATE:{1}".format(base, str(self.m_state))




