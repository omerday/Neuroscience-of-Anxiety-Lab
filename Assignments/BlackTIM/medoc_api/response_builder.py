from medoc_api.commands.r_finite_ramp_by_time import finite_ramp_by_time_response
from medoc_api.commands.r_get_status_TCU import get_statusTCU_response
from medoc_api.commands.r_get_version_command import get_version_response
from medoc_api.commands.response import response


def build_response(command_id):
    """
    Wrapper for building response to solve circular dependency
    """

    res= None

    if command_id == 19:  # get GetActiveThermode
        res = response()
    if command_id == 33:  # get status TCU
        res = get_statusTCU_response()
    if command_id == 22:  # RunTest
        res = response()
    if command_id == 27:  # ClearCommandBuffer
        res = response()
    if command_id == 37:
        res = get_version_response()
    if command_id == 41:  # SetTcuState
        res = response()
    if command_id == 47:  # StopTest
        res = response()
    if command_id == 25:  # EndTest
        res = response()
    if command_id == 45:  # SimulateResponseUnit
        res = response()
    if command_id == 28:  # FiniteRampBytime
        res = finite_ramp_by_time_response()
    
    return res