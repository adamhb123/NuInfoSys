from typing import Callable, Tuple, Dict

import betabrite
from framecontrolbytes import *
from debug import mts


def _test_function(function: Callable, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Any:
    """
    Helper method for testing functions
    :param function: Callable method to be tested
    :return: None
    """
    mts(f"Testing function: {function.__name__}", seconds=5, console_out=True, ttype=SignType.SIGN_TYPE_BETABRITE)
    result = function(*args, **kwargs)
    mts(f"Received: {result}", seconds=5, console_out=True, ttype=SignType.SIGN_TYPE_ALL_VERIFY)
    return result


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
    betabrite.send_dots(DOTS_TEST_ARROW, 11, 7, file=FileName.FILE_1)


'''
Read Method Tests
'''


def test_read_time() -> None:
    """
    Tests the read_time function
    :return: None
    """
    _test_function(betabrite.read_time)


def test_read_speaker_status() -> None:
    """
    Tests the read_speaker_status function
    :return: None
    """
    _test_function(betabrite.read_speaker_status)


def test_read_general_information() -> None:
    """
    Tests the read_general_info function
    :return: None
    """
    _test_function(betabrite.read_general_information)


def test_read_memory_pool_size() -> None:
    """
    Tests the read_memory_pool_size function
    :return: None
    """
    _test_function(betabrite.read_memory_pool_size)


def test_read_memory_configuration() -> None:
    """
    Tests the read_memory_configuration function
    :return: None
    """
    _test_function(betabrite.read_memory_configuration)


def test_read_memory_dump() -> None:
    """
    Tests the read_memory_dump function
    :return: None
    """
    _test_function(betabrite.read_memory_dump)


def test_read_day_of_week() -> None:
    """
    Tests the read_day_of_week function
    :return: None
    """
    _test_function(betabrite.read_day_of_week)


def test_read_time_format() -> None:
    """
    Tests the read_time_format function
    :return: None
    """
    _test_function(betabrite.read_time_format)


def test_read_run_time_table() -> None:
    """
    Tests the read_run_time_table function
    :return: None
    """
    _test_function(betabrite.read_run_time_table)


def test_read_serial_error_status_register() -> None:
    """
    Tests the read_run_time_table function
    :return: None
    """
    _test_function(betabrite.read_serial_error_status_register)


def test_read_network_query() -> None:
    """
    Tests the read_network_query function
    :return: None
    """
    _test_function(betabrite.read_network_query)


def test_read_run_sequence() -> None:
    """
    Tests the read_run_sequence function
    :return: None
    """
    _test_function(betabrite.read_run_sequence)


def test_read_run_day_table() -> None:
    """
    Tests the read_run_day_table function
    :return: None
    """
    _test_function(betabrite.read_run_day_table)


def test_read_counter() -> None:
    """
    Tests the read_counter function
    :return: None
    """
    _test_function(betabrite.read_counter)


def test_read_large_dots_picture_memory_configuration() -> None:
    """
    Tests the read_large_dots_picture_memory_configuration function
    :return: None
    """
    _test_function(betabrite.read_large_dots_picture_memory_configuration)


def test_read_date() -> None:
    """
    Tests the read_date function
    :return: None
    """
    _test_function(betabrite.read_date)


def test_read_temperature_offset() -> None:
    """
    Tests the read_temperature_offset function
    :return: None
    """
    _test_function(betabrite.read_temperature_offset)


def run_all_tests():
    """
    Runs all betabrite sign IO tests
    """
    mts("Testing send methods")
    [x() for x in {test_send_dots}]
    mts("Testing read methods")
    [x() for x in {test_read_time, test_read_speaker_status, test_read_general_information,
                   test_read_memory_pool_size, test_read_memory_configuration, test_read_memory_dump,
                   test_read_day_of_week, test_read_time_format, test_read_run_time_table,
                   test_read_serial_error_status_register, test_read_network_query, test_read_run_sequence,
                   test_read_run_day_table, test_read_counter, test_read_large_dots_picture_memory_configuration,
                   test_read_date, test_read_temperature_offset}]
    test_read_general_information()


if __name__ == "__main__":
    run_all_tests()
