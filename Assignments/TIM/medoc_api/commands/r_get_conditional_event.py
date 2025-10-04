from medoc_api import enums
from medoc_api.Utilities import converters
from medoc_api.commands.m_message import message
from medoc_api.commands.response import response
import logging

logger = logging.getLogger(__name__)

class event_occurence:
    def __init__(self, timestamp, token, condition, ttl, peak_temp, tag):
        self.timestamp = timestamp
        self.token = token
        self.condition = condition
        self.ttl = ttl
        self.peak_temp = peak_temp
        self.tag = tag

class get_conditional_event_response(response):
    def __init__(self):
        response.__init__(self)
        self.events = []

    def read_data(self, buffer, start_position=0):
        response.read_data(buffer, start_position)
        eventsCount = buffer[start_position]
        start_position += 1
        for i in range(eventsCount):
            timestamp = converters.to_uint_32(buffer, start_position)
            start_position += 4
            token = converters.to_uint_32(buffer, start_position)
            start_position += 4
            condition = buffer[start_position]
            start_position += 1
            ttl = buffer[start_position]
            start_position += 1
            peak_temp = 0
            if (condition == enums.EventCondition.Peak or
                condition == enums.EventCondition.PeakLow or
                condition == enums.EventCondition.TemperatureDrop or
                condition == enums.EventCondition.TemperatureRaise):
                peak_temp = converters.to_int_16(buffer, start_position)
                start_position += 2
            tag = buffer[start_position]
            start_position += 1
            event = event_occurence(timestamp, token, condition, ttl, peak_temp, tag)
            self.events.append(event)

    def response_message(self):
        logger.info(f'{str(self)}')

    def __str__(self):
        base = message.__str__(self)
        return f'RESPONSE::: {message.__str__(self)} ack code {str(self.command_ack_code)} \n\t\t\t\t\t\t\t '