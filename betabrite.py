"""Introduction, purpose, and other notes
This project is a remake of the existing InfoSys project, with the goal
of being easier to read, maintain, and use.

This code is moderately based on Jonathan Koren's betabrite.py script,
so credit goes to him for a good portion of this. Most of this was
written fairly hastily so it is not the nicest code, but she gets
the job done, and I'll try and make it nicer over time.

~brewer
"""
import time
from datetime import datetime
from enum import Enum
from typing import Union, List, Dict, Optional
from warnings import warn
import random
import serial
# pylint: disable=wildcard-import
from .framecontrolbytes import *

''' 
Configurables 
'''
CLI_TERMINAL_AND = "-"  # Animation separator
CLI_ANIMATION_PROPERTY_SEPARATOR = ","  # Animation property separator
DEFAULT_SERIAL_PORT = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0"
'''
Nonconfigurables
'''
DOTS_TEST_ARROW = b"00000080000\r00000088000\r08888888800\r08888888880\r08888888800\r00000088000\r00000080000\r"
# Note that on the BetaBrite, position does not matter at all, so setting any of these does nothing
# IT IS still required to be sent in the message packet, however
ANIMATION_POS_DICT: Dict[str, bytes] = {
    'middle': TEXT_POS_MIDDLE,
    'top': TEXT_POS_TOP,
    'bottom': TEXT_POS_BOTTOM,
    'fill': TEXT_POS_FILL
}

ANIMATION_COLOR_DICT: Dict[str, bytes] = {
    'red': TEXT_COLOR_RED,
    'green': TEXT_COLOR_GREEN,
    'amber': TEXT_COLOR_AMBER,
    'dimred': TEXT_COLOR_DIMRED,
    'brown': TEXT_COLOR_BROWN,
    'orange': TEXT_COLOR_ORANGE,
    'yellow': TEXT_COLOR_YELLOW,
    'rainbow1': TEXT_COLOR_RAINBOW1,
    'rainbow2': TEXT_COLOR_RAINBOW2,
    'mix': TEXT_COLOR_MIX,
    'autocolor': TEXT_COLOR_AUTO
}

ANIMATION_MODE_DICT: Dict[str, bytes] = {
    'rotate': MODE_ROTATE,
    'hold': MODE_HOLD,
    'flash': MODE_FLASH,
    'rollup': MODE_ROLLUP,
    'rolldown': MODE_ROLLDOWN,
    'rollleft': MODE_ROLLLEFT,
    'rollright': MODE_ROLLRIGHT,
    'wipeup': MODE_WIPEUP,
    'wipedown': MODE_WIPEDOWN,
    'wipeleft': MODE_WIPELEFT,
    'wiperight': MODE_WIPERIGHT,
    'scroll': MODE_SCROLL,
    'automode': MODE_AUTO,
    'rollin': MODE_ROLLIN,
    'rollout': MODE_ROLLOUT,
    'wipein': MODE_WIPEIN,
    'wipeout': MODE_WIPEOUT,
    'cmprsrot': MODE_CMPRSROT,
    'twinkle': MODE_TWINKLE,
    'sparkle': MODE_SPARKLE,
    'snow': MODE_SNOW,
    'interlock': MODE_INTERLOCK,
    'switch': MODE_SWITCH,
    'spray': MODE_SPRAY,
    'starburst': MODE_STARBURST,
    'welcome': MODE_WELCOME,
    'slotmachine': MODE_SLOTMACHINE,
    'newsflash': MODE_NEWSFLASH,
    'trumpet': MODE_TRUMPET,
    'thankyou': MODE_THANKYOU,
    'nosmoking': MODE_NOSMOKING,
    'drinkdrive': MODE_DRINKDRIVE,
    'animal': MODE_ANIMAL,
    'fish': MODE_FISH,
    'fireworks': MODE_FIREWORKS,
    'turbocar': MODE_TURBOCAR,
    'balloons': MODE_BALLOONS,
    'cherrybomb': MODE_CHERRYBOMB
}

MEMORY_MAP: Dict[bytes, int] = {}
# Modify MEMORY_MAP as described below and specify MemoryConfiguration.CUSTOM in relevant functions for custom mapping
'''
Here is what a custom memory map would look look like

MEMORY_MAP: Dict[bytes, int] = {
    FILE_NORMAL_RANGE[0]: 1000, # == 1000 bytes of data allocated to the first non-priority file
    FILE_NORMAL_RANGE[1]: 2000, # == 2000 bytes of data allocated to the first non-priority file
    .
    .
    .
}
'''


class MemoryConfiguration(Enum):
    """
    Memory configuration settings
    ALL_FILES_EQUAL: indicates that each of the 100+ files should share an equal amount of memory
    FIRST_FILE_MAX: lazy method, indicates that the first (non-priority) file should have all the memory
    CUSTOM: indicates that memory allocation will be defined by some collection
    """
    ALL_FILES_EQUAL = 0
    FIRST_FILE_MAX = 1
    CUSTOM = 2


def _memory_map_from_configuration(config: MemoryConfiguration):
    if config == MemoryConfiguration.FIRST_FILE_MAX:
        return {k: TOTAL_MEMORY if k == FILE_NORMAL_RANGE[0] else 0 for k in FILE_NORMAL_RANGE}
    elif config == MemoryConfiguration.ALL_FILES_EQUAL:
        return {k: TOTAL_MEMORY / len(FILE_NORMAL_RANGE) for k in FILE_NORMAL_RANGE}
    elif config == MemoryConfiguration.CUSTOM:
        if not MEMORY_MAP:
            raise MemoryConfigurationError("MemoryConfiguration.CUSTOM specified, but MEMORY_MAP not defined")
    else:
        raise Exception({
            ValueError("Inappropriate argument: 'config'"),
            MemoryConfigurationError("Inappropriate MemoryConfiguration specified")
        })


class Animation:
    """
    Object designed to represent normal animations
    """

    @staticmethod
    def _validate_parameter(parameter: Union[str, bytes], dictionary: Dict[str, bytes],
                            default_on_fail: Union[str, bytes]):
        if parameter in dictionary.keys():
            return dictionary[parameter]
        elif parameter in dictionary.values():
            return parameter
        else:
            print(f"Invalid parameter provided to 'Animation' class constructor: parameter='{parameter}', "
                  f"defaulted to '{default_on_fail}'")
            return default_on_fail

    def __init__(self, text="", mode=MODE_AUTO, color=TEXT_COLOR_AUTO, position=TEXT_POS_MIDDLE):
        self.text = text
        self.mode = self._validate_parameter(mode, ANIMATION_MODE_DICT, MODE_AUTO)
        self.color = self._validate_parameter(color, ANIMATION_COLOR_DICT, TEXT_COLOR_AUTO)
        self.position = self._validate_parameter(position, ANIMATION_POS_DICT, TEXT_POS_MIDDLE)

    def __str__(self):
        return f"Animation: text='{self.text}' mode={self.mode} color={self.color} position={self.position}"

    def __repr__(self):
        return self.__str__()

    def reset(self):
        self.text = ""
        self.mode = MODE_AUTO
        self.color = TEXT_COLOR_AUTO
        self.position = TEXT_POS_MIDDLE

    def randomize(self):
        self.mode = random.choice(list(ANIMATION_MODE_DICT.values()))
        self.color = random.choice(list(ANIMATION_COLOR_DICT.values()))
        self.position = random.choice(list(ANIMATION_POS_DICT.values()))

    def display(self):
        _transmit(DEFAULT_SERIAL_PORT, _write_file(self))

    def bytestr(self):
        return SOM + self.position + self.mode + self.color + _transcode(self.text)


def _transmit(serial_port: str, payload: bytes, addr=SIGN_ADDRESS_BROADCAST,
              ttype=SIGN_TYPE_ALL_VERIFY) -> None:
    """
    Transmits a single packet
    :param serial_port: sign port
    :param payload: packet Command Code + Data Field to transmit
    :param addr: packet Sign Address - the address of the sign. See the protocol write-up summary for more details.
    :param ttype: packet Type Code - describes the type of sign we're communicating to
    :return: None
    """
    packet = WAKEUP + SOH + ttype + addr + STX + payload + EOT
    ser = serial.Serial(serial_port, 9600, timeout=10)
    ser.write(packet)
    ser.close()


def _transmit_multi(serial_port: str, payloads: List[bytes], addr=SIGN_ADDRESS_BROADCAST,
                    ttype=SIGN_TYPE_ALL_VERIFY) -> None:
    """
    [UNTESTED]
    Transmits multiple packets (in nested packet format, as per 5.1.3 in the specification)
    :param serial_port: sign port
    :param payloads: packet Command Code + Data Field to transmit, as a list, where each item is the combined bytestring
    of each Command Code and Data Field pair
    :param addr: packet Sign Address - the address of the sign. See the protocol write-up summary for more details.
    :param ttype: packet Type Code - describes the type of sign we're communicating to
    :return: None
    """
    # This would be a cool one liner to form the packet BUT we need to have 100ms delays after <STX>'s
    # packet = WAKEUP + SOH + ttype + addr + STX + (ETX+STX).join(payloads) + ETX + EOT
    ser = serial.Serial(serial_port, 9600, timeout=10)
    # Initial wakeup
    ser.write(WAKEUP + SOH + ttype + addr)
    for payload in payloads:
        ser.write(STX)
        # 100ms wait + python's performance delay should be adequate here
        time.sleep(.1)
        ser.write(payload + ETX)
    # Signal end of packet transmission
    ser.write(EOT)
    ser.close()


def _write_file(animations: Union[List[Animation], Animation], file: bytes = FILE_PRIORITY) -> bytes:
    """Writes the given animations (which could be a single animation) in the proper payload format
    If file is anything but FILE_PRIORITY, then memory needs to be allocated and dealt with before hand
    Maybe I'll add a memory configuration function that assigns memory per some sort of input specification
    :param animations:
    :param file:
    :return:
    """
    #   Many animations
    if isinstance(animations, list):
        payload = COMMAND_WRITE_TEXT + file
        for x in range(len(animations)):
            animation = animations.pop(0)
            payload += animation.bytestr()
    #   One animation
    elif isinstance(animations, Animation):
        payload = COMMAND_WRITE_TEXT + file + animations.bytestr()
    else:
        raise ValueError(f"Invalid argument given: animations='{animations}'")
    return payload


def _configure_memory(config_mode: MemoryConfiguration = MemoryConfiguration.FIRST_FILE_MAX) -> None:
    """
    Handles file memory configuration (should be ran once on startup)
    Currently only handles TEXT files, maybe I'll make a memory map object in the future
    :param config_mode: How we should go about distributing memory
    :return: None
    """
    if config_mode == MemoryConfiguration.FIRST_FILE_MAX:
        _transmit(DEFAULT_SERIAL_PORT, MODIFY_MEMORY + FILE_NORMAL_RANGE[0] + + FILE_LOCKED)


def _transcode(msg: str) -> bytes:
    """
    Transcodes the given msg to an appropriate bytes representation
    :param msg: string to transcode
    :return: the msg's bytes representation
    """
    b = bytes(msg, 'utf-8')
    b = b.replace(b'\xc2\xb0', DEGREES)
    return b


def set_time(serial_port: str = DEFAULT_SERIAL_PORT) -> None:
    """
    [UNTESTED]
    Sets the time of day (in 24-hour format) in the sign, in the format HhMm
    :return: None
    """
    _transmit(DEFAULT_SERIAL_PORT, COMMAND_WRITE_SPECIAL + SET_TIME + bytes(datetime.now().strftime("%H%M"), 'utf-8'))


def send_dots(dots_data: bytes, file: bytes = FILE_PRIORITY, serial_port: str = DEFAULT_SERIAL_PORT) -> None:
    """
    [UNTESTED]
    Sends a SMALL DOTS PICTURE file to the sign, as per 6.4.1 in the specification
    dots_data should be formatted as such:
    2 hex bytes for height + 2 hex bytes for width + row bit pattern + carriage return
    :param file: File label to write to
    :param dots_data: DOTS data to transmit
    :param serial_port: port to transmit data to
    :return: None
    """
    _transmit(serial_port, COMMAND_WRITE_DOTS + file + dots_data)


def soft_reset(serial_port: str = DEFAULT_SERIAL_PORT):
    _transmit(serial_port, COMMAND_WRITE_SPECIAL + b"\x2c")


def send_animations(animations: List[Animation]):
    """
    Transmits the given list of animations to the betabrite sign
    :param animations: list of animations to transmit
    :return: None
    """
    #   If you want to send just one animation, you can use its 'display()' method
    # _transmit(DEFAULT_SERIAL_PORT, _write_file(animations, file=FILE_NORMAL_RANGE[0]))
    # To transmit to a non
    _transmit(DEFAULT_SERIAL_PORT, _write_file(animations, file=FILE_PRIORITY))


def _cli_parse_animations_from_string(animation_string: str) -> List[Animation]:
    """
    animation_string should be formatted as such:
    TEXT ANIMATION_MODE ANIMATION_COLOR ANIMATION_POSITION$CLI_TERMINAL_AND$NEXT_ANIMATION
    e.g. chungus cherrybomb rainbow2 None-bingus None amber None
    where '-' is replaced with the CLI_TERMINAL_AND
    """
    return _cli_parse_animations(animation_string.split(CLI_TERMINAL_AND))


def _cli_parse_animations(animations: List[str]):
    parsed_animations = []
    while len(animations) != 0:
        animget = animations.pop(0).split(CLI_ANIMATION_PROPERTY_SEPARATOR)
        animget[0] = animget[0] if animget[0] != "None" else ""
        animget[1] = ANIMATION_MODE_DICT[animget[1]] if animget[1] != "None" else MODE_AUTO
        animget[2] = ANIMATION_COLOR_DICT[animget[2]] if animget[2] != "None" else TEXT_COLOR_AUTO
        animget[3] = ANIMATION_POS_DICT[animget[3]] if animget[3] != "None" else TEXT_POS_MIDDLE
        parsed_animations.append(
            Animation(animget[0], animget[1], animget[2], animget[3]))

    return parsed_animations


def main() -> None:
    # pylint: disable=import-outside-toplevel
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "messages",
        help=f"messages to send, structured like: \n"
             f"TEXT ANIMATION_MODE ANIMATION_COLOR ANIMATION_POSITION{CLI_TERMINAL_AND}[next message or EOL]",
        nargs='+')
    args = parser.parse_args()
    # display_DOTS(None)
    animations = ' '.join(args.messages)
    animations = _cli_parse_animations_from_string(animations)
    print(animations)
    # _transmit(DEFAULT_SERIAL_PORT, _write_file(animations))


class MemoryConfigurationError(Exception):
    def __init__(self, message):
        super().__init__(message)


if __name__ == '__main__':
    main()
