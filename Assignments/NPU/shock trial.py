from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError
from mcculw.device_info import DaqDeviceInfo
import ULAO

try:
    from ui_examples_util import UIExample, show_ul_error
except ImportError:
    from .ui_examples_util import UIExample, show_ul_error

device = ULAO.ULAO01()
channel = 0
data_value = "1"  # Replace with your actual data value
#device.update_value(channel, data_value)

def shock(dev=device, channel=channel):
    print("giving shock of level: ", "1")
    dev.update_value(channel, 1)