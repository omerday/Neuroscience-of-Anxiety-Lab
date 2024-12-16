import logging

from medoc_api import enums
from medoc_api.commands.m_command import command
from medoc_api.commands.m_finite_ramp_safe_duration_command import *
from medoc_api.Utilities import temp_converter, converters

logger = logging.getLogger(__name__)


class finite_ramp_by_temperature_command(finite_ramp_safe_duration_command):

    def __init__(self):
        finite_ramp_safe_duration_command.__init__(self)
        self.m_lowMargin = 0
        self.m_highMargin = 0
        self.response = None
        self.command_id = enums.COMMAND_ID.FiniteRampByTemperature

    def build_command(self, data):
        """
        build parameters from json file
        :param data: instance of command from json file from him parameters
        :return:
        """
        if 'm_allowSafeDurationOffset' in data.keys():
            self.m_allowSafeDurationOffset = data['m_allowSafeDurationOffset']
        if 'm_isWaitForTrigger' in data.keys():
            self.m_isWaitForTrigger = data['m_isWaitForTrigger']
        if 'm_isPeakDetect' in data.keys():
            self.m_isPeakDetect = data['m_isPeakDetect']
        if 'm_isCreateTimeMark' in data.keys():
            self.m_isCreateTimeMark = data['m_isCreateTimeMark']
        if 'm_isDynamicFactor' in data.keys():
            self.m_isDynamicFactor = data['m_isDynamicFactor']
        if 'm_isAllowEmptyBuffer' in data.keys():
            self.m_isAllowEmptyBuffer = data['m_isAllowEmptyBuffer']
        if 'm_ignoreKdPidParameter' in data.keys():
            self.m_ignoreKdPidParameter = data['m_ignoreKdPidParameter']
        if 'm_isStopOnResponseUnitNo' in data.keys():
            self.m_isStopOnResponseUnitNo = data['m_isStopOnResponseUnitNo']
        if 'm_isStopOnResponseUnitYes' in data.keys():
            self.m_isStopOnResponseUnitYes = data['m_isStopOnResponseUnitYes']
        if 'm_temperature' in data.keys():
            self.m_temperature = data['m_temperature']
        if 'm_time' in data.keys():
            self.m_time = data['m_time']

    def write_data(self):
        """
        :return: count bytes was written in buffer
        """
        # need testing
        extra_data = [0x00] * 13
        command.write_data(self)
        position = 0
        # write temperature
        temp = converters.get_bytes16(temp_converter.pc2tcu(self.m_temperature))
        extra_data[position] = temp[1]
        extra_data[position+1] = temp[0]
        position += 2

        low = converters.get_bytes16(temp_converter.pc2tcu(self.m_lowMargin))
        extra_data[position] = low[1]
        extra_data[position + 1] = low[0]
        position += 2

        high = converters.get_bytes16(temp_converter.pc2tcu(self.m_highMargin))
        extra_data[position] = high[1]
        extra_data[position + 1] = high[0]
        position += 2

        tok = converters.get_bytes32(self.m_time)
        extra_data[position] = tok[3]
        extra_data[position + 1] = tok[2]
        extra_data[position + 2] = tok[1]
        extra_data[position + 3] = tok[0]
        position += 4

        # options_byte
        options_byte = 0

        options_byte = converters.set_bit(options_byte, self.WAIT_TRIGGER_BIT, self.m_isWaitForTrigger)
        options_byte = converters.set_bit(options_byte, self.PEAK_DETECT_BIT, self.m_isPeakDetect)
        options_byte = converters.set_bit(options_byte, self.CREATE_TIME_MARK_BIT, self.m_isCreateTimeMark)
        options_byte = converters.set_bit(options_byte, self.USE_DYNAMIC_FACTOR, self.m_isDynamicFactor)
        options_byte = converters.set_bit(options_byte, self.ALLOW_EMPTY_BUFFER_BIT, self.m_isAllowEmptyBuffer)
        options_byte = converters.set_bit(options_byte, self.IGNORE_KD_PID_PARAMETER_BIT, self.m_ignoreKdPidParameter)

        if self.m_allowSafeDurationOffset is not None:
            options_byte = converters.set_bit(options_byte, self.ALLOW_SAFE_DURATION_OFFSET, self.m_allowSafeDurationOffset)
        extra_data[position] = options_byte
        position += 1

        # stop_condition_byte
        stop_condition_byte = 0
        stop_condition_byte = converters.set_bit(stop_condition_byte, self.STOP_ON_YES_BIT, self.m_isStopOnResponseUnitYes)
        stop_condition_byte = converters.set_bit(stop_condition_byte, self.STOP_ON_NO_BIT, self.m_isStopOnResponseUnitNo)
        extra_data[position] = stop_condition_byte
        position += 1

        # m_conditionEventsLength
        extra_data[position] = self.m_conditionEventsLength
        position += 1

        return extra_data

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}\nPARAMETERS:\t\t\t\t\t\tTEMPERATURE: {self.m_temperature}\n\t\t\t\t\t\t' \
               f'\t\tTIME: {self.m_time} \n\t\t\t\t\t\t\t\t m_lowMargin: {self.m_lowMargin} \n\t\t\t\t\t\t\t\t ' \
               f'm_highMargin: {self.m_highMargin} '



