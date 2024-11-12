import logging

from medoc_api.Utilities import temp_converter, converters
from medoc_api.commands.response import response

logger = logging.getLogger(__name__)


class get_pid_calculation_response(response):
    def __init__(self):
        self.m_thermodeID = 0
        self.m_pidID = None
        self.m_timeStamp = None
        self.m_P = False
        self.m_I = None
        self.m_D = False
        self.m_error = 0
        self.m_setPoint = 0
        self.m_oldSetPoint = 0
        self.m_temp1 = 0
        self.m_temp2 = 0
        self.m_actTemp = 0
        self.m_dac = 0
        self.m_realTemp1 = 0
        self.m_realTemp2 = 0
        self.m_pcb = 0
        self.m_water = 0
        self.m_heatsinkTemp1 = 0
        self.m_heatsinkTemp2 = 0
        self.m_tecTemp = 0
        response.__init__(self)

    def error(self):
        return temp_converter.tcu2pc(self.m_error)

    def SetPoint(self):
        return temp_converter.tcu2pc(self.m_setPoint)

    def OldSetPoint(self):
        return temp_converter.tcu2pc(self.m_oldSetPoint)

    def Temperature1(self):
        return temp_converter.tcu2pc(self.m_temp1)

    def Temperature2(self):
        return temp_converter.tcu2pc(self.m_temp2)

    def TECTemperature(self):
        return temp_converter.tcu2pc(self.m_tecTemp)

    def realTemperature1(self):
        return temp_converter.tcu2pc(self.m_realTemp1)

    def realTemperature2(self):
        return temp_converter.tcu2pc(self.m_realTemp2)

    def pcb(self):
        return temp_converter.tcu2pc(self.m_pcb)

    def heatsink1Temp(self):
        return temp_converter.tcu2pc(self.m_heatsinkTemp1)

    def heatsink2Temp(self):
        return temp_converter.tcu2pc(self.m_heatsinkTemp2)

    def Water(self):
        return temp_converter.tcu2pc(self.m_water)

    def read_data(self, buffer, start_position=0):
        """
        read data from byte array to self
        :return:
        """
        self.m_pidID = buffer[start_position]
        start_position += 1
        self.m_timeStamp = converters.to_uint_32(buffer, start_position)
        start_position += 4
        self.m_setPoint = converters.to_int_16(buffer, start_position)
        start_position += 2
        self.m_temp1 = converters.to_int_16(buffer, start_position)
        start_position += 2
        self.m_temp2 = converters.to_int_16(buffer, start_position)
        start_position += 2
        self.m_dac = converters.to_uint_16(buffer, start_position)
        start_position += 2
        return start_position
