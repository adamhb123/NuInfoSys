import betabrite
from framecontrolbytes import *
from debug import mts

'''
Send Method Tests
'''


def test_send_dots() -> None:
    """
    Tests the send_dots function
    :return: None
    """
    DOTS_TEST_ARROW: bytes = b"00000010000\r" \
                             b"00000011000\r" \
                             b"01111111100\r" \
                             b"01111111110\r" \
                             b"01111111100\r" \
                             b"00000011000\r" \
                             b"00000010000\r"
    betabrite.send_dots(DOTS_TEST_ARROW, 11, 7, file=FileName.FILE_PRIORITY)


'''
Read Method Tests
'''


def test_read_general_information() -> None:
    """
    Tests the read_general_info function
    :return: None
    """
    mts("Testing function: read_general_information", console_out=True)
    result = betabrite.read_general_information()
    mts(f"Received: {result}", console_out=True)


def run_all_tests():
    """
    Runs all betabrite sign IO tests
    """
    mts("Testing send methods")
    test_send_dots()
    mts("Testing read methods")
    test_read_general_information()


if __name__ == "__main__":
    run_all_tests()
