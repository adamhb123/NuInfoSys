import sys
from typing import Callable, Tuple, Dict
from inspect import getmembers, isfunction

from NuInfoSys import betabrite
##rom NuInfoSys impdort config
from NuInfoSys.framecontrolbytes import *
from NuInfoSys.debug import mts


def _test_send_function(func: Callable, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> bytes:
    """
    Helper method for testing functions
    :param function: Callable method to be tested
    :return: Bytes sent in the packet
    """
    mts(f"Testing function: {func.__name__}", seconds=5, ttype=SignType.SIGN_TYPE_BETABRITE)
    result: Any = func(*args, **kwargs)
    # Should see some visual confirmation
    print(f"\tSent packet: {result}")
    return result


def _test_read_function(func: Callable, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Any:
    """
    Helper method for testing functions
    :param function: Callable method to be tested
    :return: None
    """
    mts(f"Testing function: {func.__name__}", seconds=5, ttype=SignType.SIGN_TYPE_BETABRITE)
    result = func(*args, **kwargs)
    mts(f"Received: {result}", seconds=5, ttype=SignType.SIGN_TYPE_ALL_VERIFY)
    return result


'''
Send Method Tests
'''


def test_send_dots() -> bytes:
    """
    Tests the send_dots function
    :return: Bytes sent in the packet
    """
    DOTS_TEST_ARROW: bytes = b"00000010000\r" \
                             b"00000011000\r" \
                             b"01111111100\r" \
                             b"01111111110\r" \
                             b"01111111100\r" \
                             b"00000011000\r" \
                             b"00000010000\r"
    return _test_send_function(betabrite.send_dots, DOTS_TEST_ARROW, 11, 7, file=FileName.FILE_1)


'''
Read Method Tests
'''


def test_read_time() -> None:
    """
    Tests the read_time function
    :return: None
    """
    _test_read_function(betabrite.read_time)


def test_read_speaker_status() -> None:
    """
    Tests the read_speaker_status function
    :return: None
    """
    _test_read_function(betabrite.read_speaker_status)


def test_read_general_information() -> None:
    """
    Tests the read_general_info function
    :return: None
    """
    _test_read_function(betabrite.read_general_information)


def test_read_memory_pool_size() -> None:
    """
    Tests the read_memory_pool_size function
    :return: None
    """
    _test_read_function(betabrite.read_memory_pool_size)


def test_read_memory_configuration() -> None:
    """
    Tests the read_memory_configuration function
    :return: None
    """
    _test_read_function(betabrite.read_memory_configuration)


def test_read_memory_dump() -> None:
    """
    Tests the read_memory_dump function
    :return: None
    """
    _test_read_function(betabrite.read_memory_dump)


def test_read_day_of_week() -> None:
    """
    Tests the read_day_of_week function
    :return: None
    """
    _test_read_function(betabrite.read_day_of_week)


def test_read_time_format() -> None:
    """
    Tests the read_time_format function
    :return: None
    """
    _test_read_function(betabrite.read_time_format)


def test_read_run_time_table() -> None:
    """
    Tests the read_run_time_table function
    :return: None
    """
    _test_read_function(betabrite.read_run_time_table)


def test_read_serial_error_status_register() -> None:
    """
    Tests the read_run_time_table function
    :return: None
    """
    _test_read_function(betabrite.read_serial_error_status_register)


def test_read_network_query() -> None:
    """
    Tests the read_network_query function
    :return: None
    """
    _test_read_function(betabrite.read_network_query)


def test_read_run_sequence() -> None:
    """
    Tests the read_run_sequence function
    :return: None
    """
    _test_read_function(betabrite.read_run_sequence)


def test_read_run_day_table() -> None:
    """
    Tests the read_run_day_table function
    :return: None
    """
    _test_read_function(betabrite.read_run_day_table)


def test_read_counter() -> None:
    """
    Tests the read_counter function
    :return: None
    """
    _test_read_function(betabrite.read_counter)


def test_read_large_dots_picture_memory_configuration() -> None:
    """
    Tests the read_large_dots_picture_memory_configuration function
    :return: None
    """
    _test_read_function(betabrite.read_large_dots_picture_memory_configuration)


def test_read_date() -> None:
    """
    Tests the read_date function
    :return: None
    """
    _test_read_function(betabrite.read_date)


def test_read_temperature_offset() -> None:
    """
    Tests the read_temperature_offset function
    :return: None
    """
    _test_read_function(betabrite.read_temperature_offset)


def run_all_send_tests() -> None:
    """
    Runs all betabrite sign send IO tests
    :return: None
    """
    mts("Testing send methods")
    [x[1]() for x in
     getmembers(sys.modules[__name__], lambda x: isfunction(x) and "test_send" in x.__name__ and "_" != x.__name__[0])]


def run_all_read_tests() -> None:
    """
    Runs all betabrite sign read IO tests
    :return: None
    """
    mts("Testing read methods")
    [x[1]() for x in
     getmembers(sys.modules[__name__], lambda x: isfunction(x) and "test_read" in x.__name__ and "_" != x.__name__[0])]


def run_all_tests() -> None:
    """
    Runs all betabrite sign IO tests
    :return: None
    """
    run_all_send_tests()
    run_all_read_tests()


def main() -> None:
    """
    CLI Entrypoint

    # pylint: disable=import-outside-toplevel
    import argparse
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "tests_to_run",
        help=f"test or test group to run"
    , nargs='?', default="run_all_tests")
    args: argparse.Namespace = parser.parse_args()
    tests_to_run: str = args.tests_to_run
    if config.CLI_ALLOW_TRANSMISSION:
        [x[1]() for x in getmembers(sys.modules[__name__], lambda x: isfunction(x) and tests_to_run == x.__name__)]
    mts("Testing complete")
    """
    run_all_read_tests()


if __name__ == "__main__":
    main()
