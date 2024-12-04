from enum import Enum


class TcuErrorCode(Enum):
        # <summary>
        # Ok
        # </summary>
        Ok = 0
        # <summary>
        # Thermode overheat
        # </summary>
        Error_Overheat = 0x8001
        # <summary>
        # Temperature violates safety duration table
        # </summary>
        Error_Heat_Duration = 0x8002
        # <summary>
        # Static sensor mismatch
        # </summary>
        ErrorStaticSensorMismatch = 0x8003
        # <summary>
        # Dynamic sensor mismatch
        # </summary>
        Error_Dynamic_Sensor_Mismatch = 0x8004
        # <summary>
        # Emergency disconnect fail
        # </summary>
        ErrorEmgDisconnectFail = 0x8005
        # <summary>
        # No response of Heater temperature sensor was detected
        # </summary>
        ErrorNoHeaterResponse = 0x8006
        # <summary>
        # No response of TEC temperature sensor was detected
        # </summary>
        Error_No_Tec_Response = 0x8007
        # <summary>
        # Water overheat
        # </summary>
        Error_Water_Overheat = 0x8008
        # <summary>
        # Heater sensor is short or disconnected
        # </summary>
        Error_Heater_Sensor = 0x8009
        # <summary>
        # TEC sensor is short or disconnected
        # </summary>
        Error_Tec_Sensor = 0x800A
        # <summary>
        # Water sensor is short or disconnected
        # </summary>
        Error_Water_Sensor = 0x800B
        # <summary>
        # Communication to betwwen TCU and PC lost while in Rest or Test mode
        # </summary>
        Error_Communication_Lost = 0x800C
        # <summary>
        # There are no enabled thermodes
        # </summary>
        Error_No_Enabled_Thermodes = 0x800D
        # <summary>
        # Safety cold duration limit violation
        # </summary>
        Error_Cold_Duration = 0x800E
        # <summary>
        # Thermode detection failed for CHEPS thermode
        # </summary>
        ErrorChepsThermodeMissing = 0x800F
        # <summary>
        # Thermode detection failed for ATS thermode
        # </summary>
        ErrorAtsThermodeMissing = 0x8010
        # <summary>
        # Specify current TCU state when return illegal state
        # </summary>
        Error_Illegal_State = 0x8011
        # <summary>
        # Fatal sensor mismatch
        # </summary>
        ErrorFatalSensorMismatch = 0x8012
        # <summary>
        # Go to Safe mode
        # </summary>
        ErrorDurationTable = 0x8013
        # <summary>
        # Heatsinks tempersture delta is too big
        # </summary>
        ErrorHSDeltaTooBig = 0x8015
        # <summary>
        # Thermode temperasture rate is too big
        # </summary>
        ErrorRateTooBig = 0x8016
        # <summary>
        # HS1 temperasture rate is too big
        # </summary>
        ErrorHS1RateTooBig = 0x8017
        # <summary>
        # HS2 temperasture rate is too big
        # </summary>
        ErrorHS2RateTooBig = 0x8018
        # <summary>
        # External emergency triggered
        # </summary>
        ErrorExternalEmergency = 0x8019
        # <summary>
        # Safety temperature error
        # </summary>
        SafetyTempError = 0x8020
        # <summary>
        # APID temperature error
        # </summary>
        APIDTempError = 0x8021
        # <summary>
        # Firmware internal error
        # </summary>
        FirmwareInternalError = 0x8080
        # <summary>
        # Empty command buffer
        # </summary>
        Error_Empty_Command_Buffer = 0x400C
        # <summary>
        # Time mark missed (Onset-to-onset time violation)
        # </summary>
        Error_Time_Mark_Missed = 0x400D
        # <summary>
        # Sample buffer full
        # </summary>
        Warning_Sample_Buffer_Full = 0x2001
        # <summary>
        # 
        # </summary>
        Warning_Finite_Ramp_By_Temp_Timeout = 0x2002
        # <summary>
        # Static sensor mismatch
        # </summary>
        Warning_Static_Sensor_Mismatch = 0x2003
        # <summary>
        # Watchdog caused TCU reset
        # </summary>
        Warning_Watchdog_Reset = 0x2004
        # <summary>
        # Thermode disconnected
        # </summary>
        Warning_Thermode_Disconnected = 0x2005
        # <summary>
        # TCU startup
        # </summary>
        Info_Startup = 0x2006
        # <summary>
        # Warning sensor mismatch
        # </summary>
        ErrorWarningSensorMismatch = 0x2007
        # <summary>
        # Warning thermode model mismatch
        # </summary>
        ErrorWarningThermodeModelMismatch = 0x2008
