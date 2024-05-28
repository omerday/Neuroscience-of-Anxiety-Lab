from medoc_api import crc8
import logging
from medoc_api import enums
from medoc_api.commands import m_message
from medoc_api.Utilities import converters
from medoc_api.commands.r_finite_ramp_by_temperature import finite_ramp_by_temperature_response
from medoc_api.commands.r_finite_ramp_by_time import finite_ramp_by_time_response
from medoc_api.commands.r_get_errors_command import get_errors_response
from medoc_api.commands.r_get_status_TCU import get_statusTCU_response
from medoc_api.commands.r_get_version_command import get_version_response
from medoc_api.commands.response import response

logger = logging.getLogger(__name__)

CRC_INDEX = 0
LENGTH_INDEX = 1
ID_INDEX = LENGTH_INDEX + 2
TOKEN_INDEX = ID_INDEX + 1
TAG_INDEX = TOKEN_INDEX + 4
LENGTH_EXTRA_DATA_COMMAND = TAG_INDEX + 1
# for response
ACK_CODE_INDEX = TAG_INDEX + 1
EXTRA_DATA_RESPONSE_INDEX = ACK_CODE_INDEX + 1

class command(m_message.message):

    def __init__(self):
        m_message.message.__init__(self)
        self.response = None

    def to_bytes(self):
        """
            create bytes from command
            :param command: object that need convert to bytes
        """
        if self.command_id == enums.COMMAND_ID.Undefined:
            raise ValueError("Invalid command id")
        array1 = [0x00] * m_message.MAX_LENGTH
        array1[ID_INDEX] = self.command_id.value
        if self.command_token is not None:
            tok = converters.get_bytes32(self.command_token)
            array1[TOKEN_INDEX] = tok[3]
            array1[TOKEN_INDEX + 1] = tok[2]
            array1[TOKEN_INDEX + 2] = tok[1]
            array1[TOKEN_INDEX + 3] = tok[0]
        array1[TAG_INDEX] = 0 if self.command_tag is None else self.command_tag.value
        extra_data = self.write_data()
        write_len = len(extra_data)
        i = 0
        while i < write_len:
            array1[LENGTH_EXTRA_DATA_COMMAND + i] = extra_data[i]
            i += 1
        # write command length
        command_length = TAG_INDEX + write_len + 1
        array_length = converters.get_bytes16(command_length - 1)
        array1[LENGTH_INDEX] = array_length[1]  #
        array1[LENGTH_INDEX + 1] = array_length[0]
        # write crc8
        crc = crc8.calculate(array1, CRC_INDEX + 1, command_length - 1)
        array1[CRC_INDEX] = crc
        # create array for write to device
        self.command_array = []
        if (write_len > 0):
            self.command_array = array1[0:command_length]
        else:
            self.command_array = array1[0:command_length]

        # copy to new array

    def send_message(self):
        pass

    def build_command(self, data):
        """
        build parameters from json file
        :param data: instance of command from json file from him parameters
        :return:
        """
        pass

    def write_data(self):
        """
        :param buffer: bytes array of command
        :return: array of extra data
        """
        return []

    def header_length_from_bytes(self, header):
        """
            Realizaation for TSA3 only
            :param header: response header
            :return: return command length.
        """
        length = converters.to_int_16(header, LENGTH_INDEX)
        # self.command_id = m_message.ID_TO_COMMAND[header[LENGTH_ID]]
        # self.command_token = header[LENGTH_TOKEN]
        # self.command_tag = header[LENGTH_TAG]
        return length

    def receive_response(self, header_buffer, body_buffer):
        """
        :param header_buffer: list of 4 bytes represent header response
        :param body_buffer: body response
        :return:
        """
        command_length = converters.to_u_int_16_ex(header_buffer, LENGTH_INDEX) - len(header_buffer) + 1
        buf = list(header_buffer)
        buf.extend(body_buffer[0: command_length])
        self.get_message(buf)

    def get_message(self, buffer):
        """
        :type list
        :param buffer
        :return object: response
        :Date: 2022-11-30
        :Version: 1
        :Authors: bodomus@gmail.com
        """
        crc = buffer[CRC_INDEX]
        length = converters.to_uint_16(buffer, LENGTH_INDEX)
        if length + 1 > len(buffer):
            raise ValueError(f"Invalid length of input buffer: {length + 1}  len(buffer): {len(buffer)} ")
        crcCalculated = crc8.calculate(buffer, CRC_INDEX + 1, length)
        if crc != crcCalculated:
            raise ValueError("Invalid crc code")

        if self.command_id.value != buffer[ID_INDEX]:
            raise ValueError("Invalid command id")

        # TODO create response command
        self.create_response(buffer)

    def create_response(self, buffer):
        """
            Вызывается когда получен ответ от железа для конвертации байтов в команду
            :param buffer
            :Date: 2022-11-30
            :Version: 1
            :Authors: bodomus@gmail.com
        """
        length = converters.to_uint_16(buffer, LENGTH_INDEX)
        self.build_response(self.command_id.value)
        self.response.command_id = enums.COMMAND_ID(buffer[ID_INDEX])
        self.response.command_token = converters.to_uint_32(buffer, TOKEN_INDEX)
        self.response.command_tag = enums.DEVICE_TAG(buffer[TAG_INDEX])
        self.response.command_ack_code = enums.ACKCODE(buffer[ACK_CODE_INDEX])
        if self.response.command_ack_code == enums.ACKCODE.Ok:
            self.response.read_data(buffer, EXTRA_DATA_RESPONSE_INDEX)

    def build_response(self, command_id) ->object:
        """
            Вызывается когда получен ответ от железа для конвертации байтов в команду
            :param command_id command id (int)
            :type
            :Date: 2022-11-30
            :Version: 1
            :Authors: bodomus@gmail.com
        """
        if command_id == 18:  # get GetActiveThermode
            self.response = response()
        if command_id == 19:  # get GetActiveThermode
            self.response = response()
        if command_id == 22:  # RunTest
            self.response = response()
        if command_id == 25:  # EndTest
            self.response = response()
        if command_id == 27:  # ClearCommandBuffer
            self.response = response()
        if command_id == 28:  # FiniteRampBytime
            self.response = finite_ramp_by_time_response()
        if command_id == 29:  # FiniteRampBytemperature
            self.response = finite_ramp_by_temperature_response()
        if command_id == 33:  # get status TCU
            self.response = get_statusTCU_response()
        if command_id == 35:  # GetErrors
            self.response = get_errors_response()
        if command_id == 36:  # EraseErrors
            self.response = response()
        if command_id == 37:
            self.response = get_version_response()
        if command_id == 41:  # SetTcuState
            self.response = response()
        if command_id == 45:  # SimulateResponseUnit
            self.response = response()
        if command_id == 47:  # StopTest
            self.response = response()
        if command_id == 83:  # enable termode
            self.response = response()
