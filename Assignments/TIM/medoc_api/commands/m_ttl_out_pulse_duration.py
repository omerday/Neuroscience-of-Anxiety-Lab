import logging

import medoc_api.enums as enums
from medoc_api.commands.m_command import command
from medoc_api.Utilities  import converters

class set_TTL_out_pulse_duration_command(command):
    def __init__(self, command_tag: enums.DEVICE_TAG = enums.DEVICE_TAG.Master):
        command.__init__(self, command_tag)
        self.m_channel = enums.TTLOUTChannel.TTLOUT
        self.m_duration = 0
        self.command_id = enums.COMMAND_ID.SetTTLOUTPulseDuration

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00] * 5
        extra_data[0] = self.m_channel.value
        temp = converters.get_bytes32(self.m_duration)
        extra_data[1] = temp[3]
        extra_data[2] = temp[2]
        extra_data[3] = temp[1]
        extra_data[4] = temp[0]

        return extra_data

    def build_command(self, data):
        """
        build parameters from json file
        :param data: instance of command from json file from him parameters
        :return:
        """
        if 'm_channel' in data.keys():
            self.m_channel = enums.TTLOUTChannel(data['m_channel'])
        if 'm_duration' in data.keys():
            self.m_duration = data['m_duration']

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}\nPARAMETERS\t\t\t\t\t\tm_channel = {self.m_channel}\n\t\t\t\t\t\t\t' \
               f'\tm_duration = {str(self.m_duration)}'
