

def str2bool(strValue: str) -> bool:
    """
    Converts a known set of strings to a boolean value

    Args:
        strValue:

    Returns:  the boolean value
    """
    return strValue.lower() in ("yes", "true", "t", "1", 'True')


def secureInteger(x: str):
    if x is not None and x != '':
        return int(x)
    else:
        return 0
