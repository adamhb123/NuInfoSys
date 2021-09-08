import time
import betabrite

def mts(message: str, seconds: int=5):
    """
    Message, then sleep
    :param seconds: seconds to sleep after sending the message
    :return: None
    """
    betabrite.send_animations(betabrite.Animation(message))
    time.sleep(seconds)

def read_general_information():
    betabrite._transmit(COMMAND_READ_SPECIAL + READ_GENERAL_INFORMATION)
    # wait for start of header
    # betabrite.
