# from event import Event
from medoc_api.commands.m_command import command
from medoc_api.token_holder import TokenHolder
import time
import logging
import serial
from medoc_api.commands import response

logger = logging.getLogger()

class CommandAPI:
    """
    Static Class for sending commands on demand.

    Relies on passing the serial device and communication token per send
    """

    @staticmethod
    def send_command_immediate(ser, token_holder: TokenHolder, com: command, data=None, inc_token=False) -> response:
        """
        Processed and sends the command for write and reads response in blocking mode

        :param ser: The serial interface to send to
        
        :param token_holder: The TokenHolder object for passing the active token

        :param com: A command that will be processed and sent

        :returns: None on fail or the final command's response after send and receive
        """

        com_processed = CommandAPI.process_command(token_holder.token, com, data)
        res = CommandAPI._write_command(ser, com_processed)
        if inc_token:
            token_holder.token += 1
        return res
    
    @staticmethod
    def process_command(token_raw: int, com: command, data=None) -> command:
        """
        Calls the required preperation functions on the command and returns it, also passes it the integer token 

        :param token_raw: The active token in it's value form (an integer)

        :param com: The command to be processed

        :returns: The given command after being processed
        """

        if data is not None:
            com.build_command(data)
        com.command_token = token_raw
        com.send_message()
        com.to_bytes()

        return com

    @staticmethod
    def _write_command(ser: serial.Serial, processed_command: command) -> response:
        """
        Meant to be used from within the class, use `send_command_immediate` instead

        Writes the command and reads the response in blocking mode

        :param ser: The serial interface to send to

        :param processed_command: The command to be sent, assumed to have been passed to `process_command`

        :returns: None on fail or the final command's response after send and receive
        """

        try:
            send_length = ser.write(processed_command.command_array)
            if send_length == 0:
                logger.error("Send command failed - Wrote 0 bytes")
                return None
        except serial.SerialTimeoutException:
            logger.error("Send command failed - Write timeout")
            return None

        ser.flush()

        # Wait for serial data to be received with a maximum delay of 0.5 seconds
        timeout_start = time.time()
        while ser.in_waiting < 4:
            # pass
            if time.time() >= timeout_start + 0.2:
                # print(".", end="")
                break

        try:
            header = ser.read(4)
            if len(header) < 4:
                logger.error("Read response failed - Read less than expected (4) bytes")
                return None
        except serial.SerialTimeoutException:
            logger.error("Read response failed - Read timeout")
            return None

        command_length = processed_command.header_length_from_bytes(header)

        while ser.in_waiting:
            data = ser.read(command_length)
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            try:
                processed_command.receive_response(header, data)
                processed_command.response.response_message()
            except ValueError:
                logger.error("Invalid command id for command, likely bad communication. command: `%s`", processed_command)
                return None

        return processed_command.response
        