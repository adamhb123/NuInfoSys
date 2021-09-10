import time
import betabrite


def mts(message: str, seconds: int = 5, console_out: bool = False):
    """
    Sends message to display and then sleeps for seconds
    :param message: Message to display
    :param seconds: Seconds to sleep
    """
    """
    Message, then sleep
    :param seconds: seconds to sleep after sending the message
    :return: None
    """
    betabrite.send_animations(betabrite.Animation(message, mode=betabrite.TextMode.CMPRSROT))
    if console_out:
        print(f"[MTS] {message}")
    time.sleep(seconds)
