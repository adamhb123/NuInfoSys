import time
import memory
import betabrite
from debug import mts
_MEMORY = memory.Memory()


def test_memory_clear():
    mts("Testing memory clearance...")
    _MEMORY.clear()

def test_memory_flash():
    mts("Testing memory flashing...")
    _MEMORY.flash()     

def run_all_tests(seconds_between_tests: int = 5):
    mts("Running all memory tests...")
    test_memory_clear()
    time.sleep(seconds_between_tests) 
    test_memory_flash()


if __name__=="__main__":
    run_all_tests()
