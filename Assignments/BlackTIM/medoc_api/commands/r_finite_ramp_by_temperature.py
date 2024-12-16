from medoc_api.Utilities import converters, temp_converter
from medoc_api.commands.m_message import message
from medoc_api.commands.response import response
import logging

logger = logging.getLogger(__name__)


class finite_ramp_by_temperature_response(response):
    USE_TIME_MARK_BIT = 3

    def __init__(self):
        # finite_ramp_safe_duration_command.__init__(self)
        self.m_isStopOnResponseUnitNo = None
        self.m_isStopOnResponseUnitYes = None
        self.m_ignoreKdPidParameter = None
        self.m_isAllowEmptyBuffer = None
        self.m_isDynamicFactor = None
        self.m_isCreateTimeMark = None
        self.m_isWaitForTrigger = None
        self.m_time = None
        self.m_high = None
        self.m_low = None
        self.m_temperature = 0
        self.m_isPeakDetect = None
        self.m_temperature = None
        self.m_condEventsNo = None

    def read_data(self, buffer, start_position=0):
        pass
        # count = response.read_data(buffer, start_position)
        # temperature = converters.to_int_16(buffer, start_position)
        # start_position += 2
        # self.m_temperature = temp_converter.tcu2pc(temperature)
        #
        # low = converters.to_int_16(buffer, start_position)
        # start_position += 2
        # self.m_low = temp_converter.tcu2pc(low)
        #
        # high = converters.to_int_16(buffer, start_position)
        # start_position += 2
        # self.m_high = temp_converter.tcu2pc(high)
        #
        # time = converters.to_uint_32(buffer, start_position)
        # start_position += 4
        # self.m_time = time
        #
        # optionsByte = buffer[start_position]
        # start_position += 1
        #
        # self.m_isWaitForTrigger = converters.get_bit(optionsByte, self.WAIT_TRIGGER_BIT)
        # self.m_isPeakDetect = converters.get_bit(optionsByte, self.PEAK_DETECT_BIT)
        # self.m_isCreateTimeMark = converters.get_bit(optionsByte, self.CREATE_TIME_MARK_BIT)
        # self.m_isDynamicFactor = converters.get_bit(optionsByte, self.USE_DYNAMIC_FACTOR)
        # self.m_isAllowEmptyBuffer = converters.get_bit(optionsByte, self.ALLOW_EMPTY_BUFFER_BIT)
        # self.m_ignoreKdPidParameter = converters.get_bit(optionsByte, self.IGNORE_KD_PID_PARAMETER_BIT)
        # stopConditionsByte = buffer[start_position]
        # start_position += 1
        # self.m_isStopOnResponseUnitYes = converters.get_bit(stopConditionsByte, self.STOP_ON_YES_BIT)
        # self.m_isStopOnResponseUnitNo = converters.get_bit(stopConditionsByte, self.STOP_ON_NO_BIT)
        # # TODO ConditionEventsCount = reader.ReadByte();
        # self.m_condEventsNo = buffer[start_position]
        # start_position += 1

    def __str__(self):
        return f"RESPONSE::: {message.__str__(self)} ack code {str(self.command_ack_code)} "
               # f"\n\t\t\t\t\t\t\t" \
               # f"temperature: {self.m_temperature}\n\t\t\t\t\t\t\t\t" \
               # f"m_low: {self.m_low}\n\t\t\t\t\t\t\t\t" \
               # f"m_high: {self.m_high}\n\t\t\t\t\t\t\t\t" \
               # f"m_isWaitForTrigger: {self.m_isWaitForTrigger}\n\t\t\t\t\t\t\t\t" \
               # f"m_isPeakDetect: {self.m_isPeakDetect}\n\t\t\t\t\t\t\t\t" \
               # f"m_isCreateTimeMark: {self.m_isCreateTimeMark}\n\t\t\t\t\t\t\t\t" \
               # f"m_isDynamicFactor: {self.m_isDynamicFactor}\n\t\t\t\t\t\t\t\t" \
               # f"m_isAllowEmptyBuffer: {self.m_isAllowEmptyBuffer}\n\t\t\t\t\t\t\t\t" \
               # f"m_ignoreKdPidParameter: {self.m_ignoreKdPidParameter}\n\t\t\t\t\t\t\t\t" \
               # f"m_isStopOnResponseUnitYes: {self.m_isStopOnResponseUnitYes}\n\t\t\t\t\t\t\t\t" \
               # f"m_isStopOnResponseUnitNo: {self.m_isStopOnResponseUnitNo}\n\t\t\t\t\t\t\t\t"

    def response_message(self):
        logger.info(f'{str(self)}\n')
