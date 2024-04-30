# Python API for Medoc TSA2 Device

#IMPORTANT NOTE
Prior to starting work with the Python code, open MMS software and connect to the device. Go to Hardware settings>thermode tab and  make sure the thermodes that are connected to the device are the ones enabled and set as current. This ensures the correct calibration file (LUT), PID and voltage settings are stored to the device. Unless manually changed these will remain stored on the device.
   
# Prerequisites

## Python Packages
- `pyserial` - Used for communicating with the device
- `getch` (Optional, Unix) - Used for terminal input in example

# Usage

## Codebase notes
Important points about the program:
- The main usage of the API is through the `TsaDevice` class
- The `TsaDevice` class contains mainly wrappers for commands and a few features.
- The `TsaDevice` class internally calls the static `CommandAPI` methods, which is a lower-level class that communicates directly with the device and protocol.
- The code makes use of events, which often require binding member/global functions

### C API

The codebase uses a small C library located in the `C/` folder

The C API currently consists of constants for the temperature safety table, and functions to utilize it. 
#IMPORTANT NOTE: The safety table is stored in a DLL and is not editable.

To access the C API from python, there is the `CApi` class located in `c_api.py`, which contains wrappers for the functions implemented in C.

### Events

Events are objects to connect parts of the code

The usage of an event is simple. Create an Event object, connect it to any desired functions (callbacks), and emit when desired.

Events can have either an arbitrary amount and type of parameters or specific ones via `TypedEvent`

The `TsaDevice` class has a few events, they are:
- `event_status_update` - This event is emitted on every update period of the status thread
- `event_patient_response` - This event is emitted when a patient response unit (physical device) is pressed

## Using the API

The `TsaDevice` class needs to start a status thread, which should be initialized with it's `start_status_thread` function

Managing the device state is currently required.

The possible states can be found in the `enums.SystemState` enum

Set the state with the `TsaDevice`'s `set_tcu_state` function. The `wait_for_state` parameter will rely on the status thread being active, and will halt the program until the desired state is applied to the device (this can take time).

When starting the program procedure, you should set the state to `RestMode`

To run a test, use the following procedure:

- Set the device state to `TestInit`
- Use the appropriate test function, such as `finite_ramp_by_temperature`, which is a segment of a temperature profile, from current temperature to a defined destination temperature (can be the same as in a "hold" segment) at a given change time. The destination temperature divided by the time equals the rate of temperature change. Function definition is given below:

finite_ramp_by_temperature(self,
                                    temperature,
                                    low_margain,
                                    high_margain,
                                    allow_safe_duration_offset=False, 
                                    is_wait_for_trigger=False, 
                                    is_peak_detect=False, 
                                    is_create_time_mark=False,
                                    is_dynamic_factor=False,
                                    is_allow_empty_buffer=True,
                                    ignore_kd_pid_parameter=False,
                                    is_stop_on_response_unit_no=False,
                                    is_stop_on_response_unit_yes=False,
                                    time=1000
                                    ):

legend:
destination temperture = 	           					     temperature,
lower tolerance of reaching destination =  					     low_margain,
lower tolerance of reaching destination = 					     high_margain,
do not change =                  					             allow_safe_duration_offset=False, 
use if the segment requires trigerring from an external hardware TTL to the device = is_wait_for_trigger=False, 
peak event detection = 				                                     is_peak_detect=False, 
do not change =  				                                     is_create_time_mark=False,
do not change =  			 	                                     is_dynamic_factor=False,
do not change =  				                                     is_allow_empty_buffer=True,
set to True for Pulses, False for Ramp and Hold =                                    ignore_kd_pid_parameter=False,
use for physical patient response unit feedback, yes =                               is_stop_on_response_unit_no=False,
use for physical patient response unit feedback, no =                                is_stop_on_response_unit_yes=False,
time in msec to make the temperature change required =                               time=1000

- Use the `run_test` function to start the test segment
- When you are ready to end the whole test, call the `end_test` function
- If you want to switch to another segment rather than end altogether, use the `stop_test` function instead.

When you are ready to shut down the program, use the device's `finalize` function.

# Examples

The examples can be found in `examples.py`, under the classes `Main`, `TestTemperature`, and `TestFeatures`

Please check which example is ran in the bottom lines of the program.



#Updates 09.04.2024

- Added infinite time allowed between 16degC and 40degC (in libPythonAPI.dll).
- Added current thermode command. This enables utilizing both thermodes independently by using the enable_thermode command for the thermodes participating in a test, then use set_active_thermode and set_current_thermode commands before a temperature command. 
	- self.device.set_current_thermode(enums.DEVICE_TAG.Slave) #for secondary thermode
	- self.device.set_current_thermode(enums.DEVICE_TAG.Master) #for main thermode
- Added a loop at the end of the Main class as a temporary workaround to keep the serial connection open. This may be modified to include a condition to exit the loop.
- Added self test message boxes to ensure awareness that the thermode should be removed from skin prior to a self test.
