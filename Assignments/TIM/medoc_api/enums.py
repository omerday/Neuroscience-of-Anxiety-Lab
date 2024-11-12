from enum import Enum, unique


@unique
class ThermodeType(Enum):
    CHEPS = 0
    TSA = 1
    Algometer = 2
    Vibratory = 3
    AirTSA = 4
    CoolingUnit = 5
    TSASlave = 6
    DCHEPS = 7
    Undefined = 255

    def __str__(self):
        return str(self.name)


@unique
class TsaModel(Enum):
    Large30x30 = 0
    Small16x16 = 1
    Small5x5 = 2
    Small2x2 = 3
    IntraOral = 4
    GSA = 5
    Fmri_Large30x30 = 6
    Fmri_Small16x16 = 7
    Fmri_Small5x5 = 8
    Fmri_Small2x2 = 9
    Fmri_IntraOral = 10
    Fmri_GSA = 11
    CPM_Hot = 12
    CPM_Cold = 13
    Unknown = 255

    def __str__(self):
        return str(self.name)


@unique
class HealthStatus(Enum):
    Ok = 0
    APosVoltageFailure = 1  # APOS voltage is out of range
    VPVoltageFailure = 2  # VP voltage is out of range
    VrefVoltageFailure = 4  # Vref voltage is out of range
    MTECCurrentFailure = 8  # Main TEC driver current is out of range
    RTECCurrentFailure = 16  # Reference TEC driver current is out of range
    MTECVoltageFailure = 32  # Main TEC driver voltage is out of range
    RTECVoltageFailure = 64  # Reference TEC driver voltage is out of range
    PumpCurrentFailure = 128  # Pump current is out of range
    WDTSelfTestFailureOffset = 256  # WDT self-test failed
    EmergencyButtonStatusOffset = 512  # Emergency button pressed
    WaterLevelWarningOffset = 1024  # Water level is too low
    MFanFailureOffset = 2048  # Main thermode fan rotor locked
    RFanFailureOffset = 4096  # Reference thermode fan rotor locked
    ICUFanFailureOffset = 8192  # Cooling unit fan rotor locked
    ICUPumpFailureOffset = 16384  # Cooling unit pump rotor locked
    ICUTECFailureOffset = 32768  # Cooling unit TEC doesnt respond

    def __str__(self):
        return str(self.name)


@unique
class ACKCODE(Enum):
    Ok = 0
    UnsupportedCommand = 1
    WrongCRC = 2
    IllegalParameter = 3
    IllegalState = 4
    ThermodeDisabled = 5
    IllegalCommandSequence = 6
    BufferFull = 7
    NoDataExists = 8
    DataAlreadyExists = 9
    Fail = 10  # Error during process command
    WrongFlashAddress = 11  # Error during process command
    WrongSize = 12  # Error during process command
    Undefined = 255

    def __str__(self):
        return str(self.name)


@unique
class SystemState(Enum):
    SafeMode = 0
    SelfTest = 1
    RestMode = 2
    TestInit = 3
    TestRun = 4
    TestPaused = 5
    Engineering = 6
    FirmwareUpdate = 7
    WritingBlackBox = 8

    def __str__(self):
        return str(self.name)


class DEVICE_TAG(Enum):
    Master = 0
    Slave = 1

    def __str__(self):
        return str(self.name)


@unique
class COMMAND_ID(Enum):
    Undefined = -1
    ProtocolError = 0
    SetActiveThermode = 18
    GetActiveThermode = 19
    RunTest = 22
    EndTest = 25
    ClearCommandBuffer = 27
    FiniteRampByTime = 28
    FiniteRampByTemperature = 29
    InfiniteRamp = 30
    GetStatusTCU = 33
    GetErrors = 35
    EraseErrors = 36
    GetVersion = 37
    SetTcuState = 41
    SimulateResponseUnit = 45
    StopTest = 47
    GetCurrentPID = 70
    EnableThermode = 83
    GetThermodeState = 84
    FiniteRampByRate = 85

    def __str__(self):
        return str(self.name)


class DeviceType(Enum):
    Undefined = 0
    TCU = 1
    CTS = 2
    Algometer = 3
    TSA2 = 4
    CTSA = 5
    VSA3000 = 6
    CPM = 7
    TSA3 = 8
    TSA3Air = 9

    def __str__(self):
        return str(self.name)

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

    def __str__(self):
        return str(self.name)
