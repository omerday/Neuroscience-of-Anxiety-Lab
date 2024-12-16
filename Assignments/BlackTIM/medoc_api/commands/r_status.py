import logging
from medoc_api.commands.response import response

logger = logging.getLogger(__name__)


class get_status_response(response):
    PROTOCOL_MAX_SAMPLES = 99
    SYSTEM_STATE_MASK = 0x0f
    SYSTEM_STATUS_BIT_CURRENT_THERMODE1 = 5
    SYSTEM_STATUS_BIT_ERROR = 6
    SYSTEM_STATUS_BIT_SAFETY_STATUS_ON = 7
    NA = "N/A"

    def __init__(self):
        self.m_timestamp = 0
        self.m_systemState =None
        self.m_currentThermode = None
        self.m_isError = False
        self.m_errorStatus = None
        self.m_isSafetyStatusOn = False
        self.m_version = 0
        self.m_commandBufferFreeSpace = 0
        self.m_temperatureBufferStartTime = 0
        self.m_executingCommandToken = 0
        self.m_slave_commandBufferFreeSpace = 0
        self.m_slave_temperatureBufferStartTime = 0
        self.m_slave_executingCommandToken = 0
        response.__init__(self)
