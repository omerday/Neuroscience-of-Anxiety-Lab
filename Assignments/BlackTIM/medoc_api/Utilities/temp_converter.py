TCU_TO_PC = 0.01;


def pc2tcu(val: float) -> int:
    """
    convert temperature
    :param val: temperature
    :return:
    """
    val /= TCU_TO_PC
    if val >= 0:
        return int(val + 0.5)
    else:
        return int(val - 0.5)


# need test
def tcu2pc(val):
    return val * TCU_TO_PC
