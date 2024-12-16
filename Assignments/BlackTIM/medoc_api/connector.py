import serial
import time
import logging
import json
import os
import sys
from medoc_api.token_holder import TokenHolder
from medoc_api.commands.m_getVersion_command import getVersion_command
from medoc_api.command_api import CommandAPI
from medoc_api.commands.response import response
from medoc_api import enums

logger = logging.getLogger(__name__)

from medoc_api.commands.m_getstatusTCU_command import get_status_TCU_command

class connector:
    MAX_PORT_DEFAULT = 20

    def __init__(self, path_to_prefernces=None, auto_detect=False, token_holder: TokenHolder=None):
        self.tunnel = self.create_com_port(path_to_prefernces, auto_detect=auto_detect, token_holder=token_holder)
        # self.tunnel.baudrate = 115200
        # self.tunnel.port = 'COM3'
        # self.tunnel.timeout = 0.5
        # self.tunnel.write_timeout = 0.5
        
        if self.tunnel == None:
            print("Error! Connector tunnel failed to create")
            return
        if not self.tunnel.is_open:
            self.tunnel.open()
        logger.info(f"Connector to {self.tunnel.port} port was successfully created\n\n")

    def finalize(self):
        if self.tunnel is not None and self.tunnel.is_open:
            self.tunnel.close()

    def get_com_port(self):
        return self.tunnel

    def find_com_port(self, token_holder: TokenHolder, min_port=0, max_port=MAX_PORT_DEFAULT, settings:dict=None) -> serial.Serial:
        """
        Auto detect and return the correct port for the TSA Device
        
        :param token_holder: The token holder object required for sending commands
        
        :param min_port: The starting port for the search, default is 0 (all ports)

        :param max_port: The final port to check, all ports between min_port and max_port will be tested until the correct is found
        
        :param settings: The settings for the interface including baudrate, timeout, etc.
        
        :returns: The correct serial port if found, else None
        """

        com = min_port
        valid_receive = False
        ser: serial.Serial = None
        
        while not valid_receive and com <= max_port:
            # Attempt to connect to a serial port with low timeout for faster iteration
            try:
                if settings:
                    if sys.platform == "win32":
                        ser = serial.Serial(
                            port=f"COM{com}",
                            baudrate=settings['baudrate'],
                            timeout=0.2,
                            write_timeout=0.2
                            )
                    elif "linux" in sys.platform:
                        ser = serial.Serial(
                            port=f"/dev/ttyUSB{com}",
                            baudrate=settings['baudrate'],
                            timeout=0.2,
                            write_timeout=0.2
                            )

                else:
                    if sys.platform == "win32":
                        ser = serial.Serial (
                            port=f"COM{com}",
                            timeout=0.2
                            )
                    elif "linux" in sys.platform:
                        ser = serial.Serial (
                            port=f"/dev/ttyUSB{com}",
                            timeout=0.2
                            )

            except serial.SerialException:
                com += 1
                continue
            
            # Once connected send the get version command as a test
            get_version_cmd = getVersion_command()
            res: response = CommandAPI.send_command_immediate(ser, token_holder, get_version_cmd, inc_token=True)

            # Check that the command went through and we got a response
            if res is not None and res.command_ack_code == enums.ACKCODE.Ok:
                # Make sure the port is closed before reopening
                if ser is not None and ser.is_open:
                    ser.close()

                # Create the serial port with the correct timeout settings
                if settings:
                    if sys.platform == "win32":
                        ser = serial.Serial(
                            port=f"COM{com}",
                            baudrate=settings['baudrate'],
                            timeout=settings['timeout'],
                            write_timeout=settings['write_timeout'],
                            )
                    elif "linux" in sys.platform:
                        ser = serial.Serial(
                            port=f"/dev/ttyUSB{com}",
                            baudrate=settings['baudrate'],
                            timeout=settings['timeout'],
                            write_timeout=settings['write_timeout'],
                            )
                else:
                    if sys.platform == "win32":
                        ser = serial.Serial (
                            port=f"COM{com}",
                            timeout=2.0
                            )
                    elif "linux" in sys.platform:
                        ser = serial.Serial (
                            port=f"/dev/ttyUSB{com}",
                            timeout=2.0
                            )

                break # Finish searching since we have the correct port
            
            # If we got here the latest port was invalid so set to None and cycle to the next
            if ser is not None and ser.is_open:
                ser.close()

            ser = None
            com += 1
        
        # Return the final serial interface which is either the correct port or None
        return ser

    def create_com_port(self, path_to_preferences=None, auto_detect=False, token_holder: TokenHolder=None) -> serial.Serial:
        """
        Creates a serial connection and returns it

        :param path_to_preferences: Optional paramter for loading the COM Port settings from file

        :param auto_detect: Whether to scan for the correct port automatically. Relies on token_holder being provided

        :param token_holder: The main TokenHolder object that will progress the token on command send. Required for automatic COM Port detection

        :returns: None if no compatible serial connection was found or the result serial connection
        """
        data = self.read_comport_preferences(path_to_preferences)
        if auto_detect and token_holder:
            if data:
                auto = self.find_com_port(token_holder, settings=data)
            else:
                auto = self.find_com_port(token_holder)
            
            return auto

        try:
            if data is None:
                if sys.platform == "win32":
                    return serial.Serial(
                        port='COM5',
                        baudrate=9600,
                        timeout=0.5,
                        writeTimeout=0.5
                    )
                elif "linux" in sys.platform:
                    return serial.Serial(
                        port='/dev/ttyUSB0',
                        baudrate=9600,
                        timeout=0.5,
                        writeTimeout=0.5
                    )

            else:
                if sys.platform == "win32":
                    return serial.Serial(
                        port=data['port'],
                        baudrate=data['baudrate'],
                        timeout=data['timeout'],
                        write_timeout=data['write_timeout'],
                    )
                elif "linux" in sys.platform:
                    return serial.Serial(
                        port=f"/dev/{data['port']}",
                        baudrate=data['baudrate'],
                        timeout=data['timeout'],
                        write_timeout=data['write_timeout'],
                    )
                else:
                    return serial.Serial(
                        port=data['port'],
                        baudrate=data['baudrate'],
                        timeout=data['timeout'],
                        write_timeout=data['write_timeout'],
                    )

        except serial.SerialException as e:
            if "linux" in sys.platform:
                if e.errno == 13:
                    raise OSError("Permission to port denied, please allow your user access to tty")
            else:
                raise serial.SerialException("No COM Port found! Try adjusting `preferences.json`")

    def read_comport_preferences(self, path: object) -> object:
        """ get com port preferences
        :type path: object
        :param path: #path to com port json file preferences
        :return object: {'port':' 'baudrate':' "parity":' "stopbits":' "bytesize":}
        :Date: 2022-11-27
        :Version: 1
        :Authors: bodomus@gmail.com
        """
        if not os.path.isfile(path):
            raise Exception("invalid file path {!r}".format(path))
        logger.info("read port preferences from file %s", path)
        with open(path) as json_file:
            data = json.load(json_file)
            return {'port': data['port'], 'baudrate': data['baudrate'], "parity": data['parity'],
                    "write_timeout": data['write_timeout'], "bytesize": data['bytesize'], "timeout": data['timeout']}

if __name__ == "__main__":
    with serial.Serial() as ser:
        ser.baudrate = 115200
        ser.port = 'COM3'
        ser.timeout = 0.5
        ser.write_timeout = 0.5
        # ser.rtscts = True
        ser.open()
        # time.sleep(2)
        l = [118, 0, 8, 37, 0, 0, 0, 2, 0, 10, 13]
        # m = [31, 31, 38, 20, 30, 20, 38, 20, 33, 37, 20, 30, 20, 30, 20, 30, 20, 32, 20, 30]

        while 1:
            if not ser.is_open:
                ser.open()
            time.sleep(1)
            length = ser.write(l)
            print(f'Send {length} bytes')
            # ser.flush()

            r = ser.read(4)
            # print(f'R={r} length: {len(r)}')
            # ser.read_until(size=10)
            while ser.in_waiting:
                data = ser.readline().decode("ascii")
                print(f'Data={data} length: {len(data)}')

            ser.close()
            if not ser.is_open:
                print('port close')
