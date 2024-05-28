import logging
from medoc_api import enums
from medoc_api.Utilities import temp_converter, converters
from medoc_api.commands.m_message import message
from medoc_api.enums import COMMAND_ID
from medoc_api.commands.r_get_pid_calculation_response import get_pid_calculation_response
from medoc_api.commands.r_status import get_status_response

logger = logging.getLogger(__name__)


class get_statusTCU_response(get_status_response):
    SYSTEM_STATUS_BIT_WAIT_FOR_TRIGGER = 4

    IO_STATE_BIT_RESPONSE_UNIT_YES_ON = 0
    IO_STATE_BIT_RESPONSE_UNIT_NO_ON = 1
    IO_STATE_BIT_EXTERNAL_TRIGGER_ON = 2
    IO_STATE_BIT_CONDITION_EVENT = 7

    STATUS_WORD_FAN0 = 1
    STATUS_WORD_FAN1 = 2
    STATUS_WORD_FAN = 4
    STATUS_WORD_APID = 8
    STATUS_WORD_SAFETY = 16
    STATUS_WORD_LED1 = 32
    STATUS_WORD_LED2 = 64
    STATUS_WORD_LED3 = 128
    STATUS_WORD_TEC_IN = 256
    STATUS_WORD_HS1_IN = 512
    STATUS_WORD_HS2_IN = 1024
    STATUS_WORD_CPU_ALIVE = 2048
    STATUS_WORD_SAFETY_MODE0 = 4096
    STATUS_WORD_SAFETY_MODE1 = 8192

    def __init__(self):
        # super(command, self).__init__()
        get_status_response.__init__(self)
        self.m_isWaitForTrigger = False
        self.m_covas = None
        self.m_isResponseUnitYesOn = False
        self.m_isResponseUnitNoOn = False
        self.m_isExternalTriggerOn = False
        self.m_externalTriggerTimestamp = None
        self.m_isConditionEvent = False
        self.m_conditionEvents = None
        self.m_eventBufferFreeSpace = None
        self.m_heaterTemperature = None
        self.m_tecTemperature = None
        self.m_waterTemperature = 0.0
        self.m_pcbTemperature = 0.0
        self.m_heatsink1Temperature = 0.0
        self.m_heatsink2Temperature = 0.0
        self.m_stateWord = 0
        self.m_chepsResponse = 0.0
        self.m_atsResponse = 0.0
        self.response = None
        self.command_id = COMMAND_ID.GetStatusTCU

        # bit 0 - main thermode enabled / disabled
        # bit 1 - ref thermode enabled / disabled
        # bit 4 - CHEPS type is expected
        # bit 5 - ATS is expected
        # bit 6 - CHEPS is detected
        # bit 7 - ATS is detected

        self.m_thermodeDetection = None
        self.m_slaveDeviceStatus = None
        self.m_slave_tecTemperature = None
        self.m_slave_waterTemperature = 0.0
        self.m_slave_isWaitForTrigger = False
        self.m_pid_data = None
        self.m_slave_pid_data = None
        self.m_slave_eventBufferFreeSpace = False
        self.m_healthStatus = None
        self.m_mainThermodeModel = None
        self.m_refThermodeModel = None

        # logging.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])

    def read_data(self, buffer, start_position):
        """
        read data from byte array to self
        :param buffer: array of data from device
        :return: count bytes read
        """
        current_position = start_position
        get_status_response.read_data(self, buffer, current_position)

        self.m_timestamp = converters.to_uint_32(buffer, start_position)
        start_position += 4
        self.m_temperatureBufferStartTime = converters.to_uint_32(buffer, start_position)
        start_position += 4
        self.m_executingCommandToken = converters.to_uint_32(buffer, start_position)
        start_position += 4
        m_system_status_byte = buffer[start_position]
        start_position += 1
        self.m_systemState = m_system_status_byte & self.SYSTEM_STATE_MASK
        self.m_isWaitForTrigger = converters.get_bit(m_system_status_byte, self.SYSTEM_STATUS_BIT_WAIT_FOR_TRIGGER)
        self.m_currentThermode = converters.get_bit(m_system_status_byte, self.SYSTEM_STATUS_BIT_CURRENT_THERMODE1)
        self.m_isError = converters.get_bit(m_system_status_byte, self.SYSTEM_STATUS_BIT_ERROR)
        self.m_covas = buffer[start_position]
        start_position += 1
        ioStateByte = buffer[start_position]
        start_position += 1
        self.m_isResponseUnitYesOn = converters.get_bit(ioStateByte, self.IO_STATE_BIT_RESPONSE_UNIT_YES_ON)
        self.m_isResponseUnitNoOn = converters.get_bit(ioStateByte, self.IO_STATE_BIT_RESPONSE_UNIT_NO_ON)
        self.m_isExternalTriggerOn = converters.get_bit(ioStateByte, self.IO_STATE_BIT_EXTERNAL_TRIGGER_ON)
        self.m_isConditionEvent = converters.get_bit(ioStateByte, self.IO_STATE_BIT_CONDITION_EVENT)
        self.m_commandBufferFreeSpace = buffer[start_position]
        start_position += 1
        self.m_eventBufferFreeSpace = buffer[start_position]
        start_position += 1
        heaterQuantity = buffer[start_position]
        start_position += 1

        # m_heaterTemperature parser
        # for (int i = 0; i < heaterQuantity; i++)
        #     this.HeaterTemperature.Add(TempConverter.TCU2PC(reader.ReadInt16()));
        self.m_heaterTemperature = []
        for x in range(0, heaterQuantity):
            temp = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_heaterTemperature.append(temp_converter.tcu2pc(temp))

        # m_tecTemperature  parser
        # for (int i = 0; i < tecQuantity; i++)
        #     this.TecTemperature.Add(TempConverter.TCU2PC(reader.ReadInt16()));
        tec_quantity = buffer[start_position]
        start_position += 1
        self.m_tecTemperature = []
        for x in range(0, tec_quantity):
            tec = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_heaterTemperature.append(temp_converter.tcu2pc(tec))

        if self.m_currentThermode == enums.ThermodeType['AirTSA']:
            val = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_heatsink1Temperature = temp_converter.tcu2pc(val)

            val = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_heatsink2Temperature = temp_converter.tcu2pc(val)

            self.m_stateWord = converters.to_u_int_16_ex(buffer, start_position)
            start_position += 2

            # this.IsSafetyStatusOn = (this.m_stateWord & STATUS_WORD_SAFETY) != 0 ? true: false;
            self.m_isSafetyStatusOn = True if self.m_stateWord & self.STATUS_WORD_SAFETY != 0 else False
        else:
            val = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_waterTemperature = temp_converter.tcu2pc(val)

            val = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_pcbTemperature = temp_converter.tcu2pc(val)

            self.m_thermodeDetection = buffer[start_position]
            start_position += 1
            self.m_isSafetyStatusOn = converters.get_bit(m_system_status_byte, self.SYSTEM_STATUS_BIT_SAFETY_STATUS_ON)

        self.m_version = buffer[start_position]
        start_position += 1
        if self.m_version == 5:
            val = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_chepsResponse = temp_converter.tcu2pc(val)
            val = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_atsResponse = temp_converter.tcu2pc(val)

        # TODO Here check on TSA3 based device
        val = buffer[start_position]
        start_position += 1
        self.m_mainThermodeModel = val
        val = buffer[start_position]
        start_position += 1
        self.m_refThermodeModel = val

        cnt = buffer[start_position]
        start_position += 1
        self.m_slave_tecTemperature = []
        for x in range(0, cnt):
            temp = converters.to_int_16(buffer, start_position)
            start_position += 2
            self.m_slave_tecTemperature.append(temp_converter.tcu2pc(temp))

        temp = converters.to_int_16(buffer, start_position)
        start_position += 2
        self.m_slave_waterTemperature = temp_converter.tcu2pc(temp)

        cnt = buffer[start_position]
        start_position += 1
        self.m_pid_data = []
        for x in range(0, cnt):
            # TODO Need implementation new GetPIDCalculationsResponse(reader, type)
            pid_position = start_position
            pid_response = get_pid_calculation_response()
            start_position = pid_response.read_data(buffer, pid_position)
            self.m_pid_data.append(pid_response)

        cnt = buffer[start_position]
        start_position += 1
        self.m_slave_pid_data = []
        for x in range(0, cnt):
            # TODO Need implementation new GetPIDCalculationsResponse(reader, type)
            pid_position = start_position
            slave_pid_response = get_pid_calculation_response()
            start_position = slave_pid_response.read_data(buffer, pid_position)
            self.m_slave_pid_data.append(slave_pid_response)

        self.m_slave_temperatureBufferStartTime = converters.to_uint_32(buffer, start_position)
        start_position += 4
        self.m_slave_executingCommandToken = converters.to_uint_32(buffer, start_position)
        start_position += 4
        self.m_slave_commandBufferFreeSpace = buffer[start_position]
        start_position += 1
        self.m_slave_eventBufferFreeSpace = buffer[start_position]
        start_position += 1
        self.m_healthStatus = converters.to_uint_16(buffer, start_position)
        start_position += 2
        self.m_slave_isWaitForTrigger = buffer[start_position]
        start_position += 1
        return start_position - current_position

    def get_state(self):
        return self.m_systemState

    def get_temp(self):
        if len(self.m_heaterTemperature) == 0:
            return 0

        return sum(self.m_heaterTemperature) / len(self.m_heaterTemperature)

    def get_temp_slave(self):
        if len(self.m_slave_tecTemperature) == 0:
            return 0

        return sum(self.m_slave_tecTemperature) / len(self.m_slave_tecTemperature)

    def response_message(self):
        logger.info(f'{str(self)}')
        pass

    def __str__(self):
        base = str(message.__str__(self))
        tec_temperature = 0 if self.m_tecTemperature is None else len(self.m_tecTemperature)
        heater_temperature = 0 if self.m_heaterTemperature is None else len(self.m_heaterTemperature)
        system_state = enums.SystemState(self.m_systemState)
        info = f"RESPONSE::: {base}\n\t\t\t\t\t\t\t Timestamp: {self.m_timestamp}" \
               f"\n\t\t\t\t\t\t\t Current thermode: {self.m_currentThermode}" \
               f"\n\t\t\t\t\t\t\t TCU state:{str(system_state)}" \
               f"\n\t\t\t\t\t\t\t Heater temperatures count: {heater_temperature}" \
               f"\n\t\t\t\t\t\t\t Heater temperatures: {self.get_temp()}" \
               f"\n\t\t\t\t\t\t\t TEC temperatures count: {tec_temperature}" \
               f"\n\t\t\t\t\t\t\t Slave TEC temperature: {self.get_temp_slave()}" \
               f"\n\t\t\t\t\t\t\t Water temperature: {self.m_waterTemperature}" \
               f"\n\t\t\t\t\t\t\t COVAS: {self.m_covas}" \
               f"\n\t\t\t\t\t\t\t External Trigger: {self.m_isExternalTriggerOn}" \
               f"\n\t\t\t\t\t\t\t External Trigger Timestamp: {self.m_externalTriggerTimestamp}" \
               f"\n\t\t\t\t\t\t\t Patient Response Yes Button: {self.m_isResponseUnitYesOn}" \
               f"\n\t\t\t\t\t\t\t Patient Response No Button: {self.m_isResponseUnitNoOn}" \
               f"\n\t\t\t\t\t\t\t Is_Error: {self.m_isError}\n "
        return info
