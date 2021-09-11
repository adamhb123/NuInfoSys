import time
import betabrite
from framecontrolbytes import *


def mts(message: str, seconds: int = 5, console_out: bool = False, file: FileName = FileName.FILE_PRIORITY):
    """
    Sends message to display and then sleeps for seconds
    :param message: Message to display
    :param seconds: Seconds to sleep
    :param console_out: Whether or not to print to console
    :param file: File to write to
    """
    """
    Message, then sleep
    :param seconds: seconds to sleep after sending the message
    :return: None
    """
    betabrite.send_animations(betabrite.Animation(message, mode=betabrite.TextMode.CMPRSROT), file=file)
    if console_out:
        print(f"[MTS] {message}")
    time.sleep(seconds)
