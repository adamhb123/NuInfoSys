import betabrite
from debug import mts


def test_read_general_information():
    """
    Tests the read_general_info function
    """
    mts("Testing function: read_general_information", console_out=True)
    result = betabrite.read_general_information()
    mts(f"Received: {result}", console_out=True)


def run_all_tests():
    """
    Runs all betabrite sign IO tests
    """
    test_read_general_information()


if __name__ == "__main__":
    run_all_tests()
