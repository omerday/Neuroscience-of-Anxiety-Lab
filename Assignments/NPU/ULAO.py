from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError
from mcculw.device_info import DaqDeviceInfo

try:
    from ui_examples_util import UIExample, show_ul_error
except ImportError:
    from .ui_examples_util import UIExample, show_ul_error
import time


class ULAO01(UIExample):
    def __init__(self, board_num=0, use_device_detection=True):
        super(ULAO01, self).__init__()

        self.board_num = board_num

        try:
            if use_device_detection:
                self.configure_first_detected_device()

            self.device_info = DaqDeviceInfo(self.board_num)
            self.ao_info = self.device_info.get_ao_info()
            if not self.ao_info.is_supported:
                print("AO is not supported on this device.")
        except ULError:
            print("An error occurred while initializing the device.")

    def update_value(self, channel, data_value):
        ao_range = self.ao_info.supported_ranges[0]
        print(data_value)

        raw_value = ul.from_eng_units(self.board_num, ao_range, data_value)

        try:
            ul.a_out(self.board_num, channel, ao_range, raw_value)
            time.sleep(0.001)
            raw_value = ul.from_eng_units(self.board_num, ao_range, 0.0)
            ul.a_out(self.board_num, channel, ao_range, raw_value)

        except ULError as e:
            show_ul_error(e)