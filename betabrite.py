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
import random
from serial import Serial
# pylint: disable=wildcard-import
from framecontrolbytes import *
from memory import *

'''
Configurables
'''
CLI_ALLOW_TRANSMISSION: bool = False
CLI_TERMINAL_AND: str = "-"  # Animation separator
CLI_ANIMATION_PROPERTY_SEPARATOR: str = ","  # Animation property separator
SERIAL_PORT: str = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0"
'''
Nonconfigurables
'''
DOTS_TEST_ARROW: bytes = b"00000080000\r00000088000\r08888888800\r08888888880\r08888888800\r00000088000\r00000080000\r"
# Note that on the BetaBrite, position does not matter at all, so setting any of these does nothing
# IT IS still required to be sent in the message packet, however
ANIMATION_POS_DICT: Dict[str, bytes] = {
    'middle': TextPosition.TEXT_POS_MIDDLE,
    'top': TextPosition.TEXT_POS_TOP,
    'bottom': TextPosition.TEXT_POS_BOTTOM,
    'fill': TextPosition.TEXT_POS_FILL
}

ANIMATION_COLOR_DICT: Dict[str, bytes] = {
    'red': TextColor.TEXT_COLOR_RED,
    'green': TextColor.TEXT_COLOR_GREEN,
    'amber': TextColor.TEXT_COLOR_AMBER,
    'dimred': TextColor.TEXT_COLOR_DIMRED,
    'brown': TextColor.TEXT_COLOR_BROWN,
    'orange': TextColor.TEXT_COLOR_ORANGE,
    'yellow': TextColor.TEXT_COLOR_YELLOW,
    'rainbow1': TextColor.TEXT_COLOR_RAINBOW1,
    'rainbow2': TextColor.TEXT_COLOR_RAINBOW2,
    'mix': TextColor.TEXT_COLOR_MIX,
    'autocolor': TextColor.TEXT_COLOR_AUTO
}

ANIMATION_MODE_DICT: Dict[str, bytes] = {
    'rotate': TextMode.MODE_ROTATE,
    'hold': TextMode.MODE_HOLD,
    'flash': TextMode.MODE_FLASH,
    'rollup': TextMode.MODE_ROLLUP,
    'rolldown': TextMode.MODE_ROLLDOWN,
    'rollleft': TextMode.MODE_ROLLLEFT,
    'rollright': TextMode.MODE_ROLLRIGHT,
    'wipeup': TextMode.MODE_WIPEUP,
    'wipedown': TextMode.MODE_WIPEDOWN,
    'wipeleft': TextMode.MODE_WIPELEFT,
    'wiperight': TextMode.MODE_WIPERIGHT,
    'scroll': TextMode.MODE_SCROLL,
    'automode': TextMode.MODE_AUTO,
    'rollin': TextMode.MODE_ROLLIN,
    'rollout': TextMode.MODE_ROLLOUT,
    'wipein': TextMode.MODE_WIPEIN,
    'wipeout': TextMode.MODE_WIPEOUT,
    'cmprsrot': TextMode.MODE_CMPRSROT,
    'twinkle': TextMode.MODE_TWINKLE,
    'sparkle': TextMode.MODE_SPARKLE,
    'snow': TextMode.MODE_SNOW,
    'interlock': TextMode.MODE_INTERLOCK,
    'switch': TextMode.MODE_SWITCH,
    'spray': TextMode.MODE_SPRAY,
    'starburst': TextMode.MODE_STARBURST,
    'welcome': TextMode.MODE_WELCOME,
    'slotmachine': TextMode.MODE_SLOTMACHINE,
    'newsflash': TextMode.MODE_NEWSFLASH,
    'trumpet': TextMode.MODE_TRUMPET,
    'thankyou': TextMode.MODE_THANKYOU,
    'nosmoking': TextMode.MODE_NOSMOKING,
    'drinkdrive': TextMode.MODE_DRINKDRIVE,
    'animal': TextMode.MODE_ANIMAL,
    'fish': TextMode.MODE_FISH,
    'fireworks': TextMode.MODE_FIREWORKS,
    'turbocar': TextMode.MODE_TURBOCAR,
    'balloons': TextMode.MODE_BALLOONS,
    'cherrybomb': TextMode.MODE_CHERRYBOMB
}
# Some of these may be the same as their bytes counterparts, but whatever
# https://www.utf8-chartable.de/unicode-utf8-table.pl
# let a = document.querySelectorAll(".utf8");
# a.forEach(elem => elem.innerHTML = elem.innerHTML.replace(' ','').replaceAll('0x','\\x'))
TextCharacterTranslationDict: Dict[bytes, bytes] = {
    b'\x0a': TextCharacter.LF,
    b'\x0d': TextCharacter.CR,
    b'\xc2\xa2': TextCharacter.CENTS,
    b'\xe2\x80\x89': TextCharacter.HALF_SPACE,
    b'\xe2\x96\xa1': TextCharacter.BLOCK_CHAR,
    b'\xc3\x87': TextCharacter.C_CEDILLA,
    b'\xc3\xbc': TextCharacter.u_DIAERESIS,
    b'\xc3\xa8': TextCharacter.e_GRAVE,
    b'\xc3\xa2': TextCharacter.a_CIRCUMFLEX,
    b'\xc3\xa4': TextCharacter.a_DIAERESIS,
    b'\xc3\xa1': TextCharacter.a_ACUTE,
    b'\xc3\xa5': TextCharacter.a_RING_ABOVE,
    b'\xc3\xa7': TextCharacter.c_CEDILLA,
    b'\xc3\xaa': TextCharacter.e_CIRCUMFLEX,
    b'\xc3\xab': TextCharacter.e_DIAERESIS,
    b'\xc3\xaf': TextCharacter.i_DIAERESIS,
    b'\xc3\xae': TextCharacter.i_CIRCUMFLEX,
    b'\xc3\xac': TextCharacter.i_GRAVE,
    b'\xc3\x84': TextCharacter.A_DIAERESIS,
    b'\xc3\x85': TextCharacter.A_RING_ABOVE,
    b'\xc3\x89': TextCharacter.E_ACUTE,
    b'\xc3\xa6': TextCharacter.ae_LIGATURE,
    b'\xc3\x86': TextCharacter.AE_LIGATURE,
    b'\xc3\xb4': TextCharacter.o_CIRCUMFLEX,
    b'\xc3\xb6': TextCharacter.o_DIAERESIS,
    b'\xc3\xb2': TextCharacter.o_GRAVE,
    b'\xc3\xbb': TextCharacter.u_CIRCUMFLEX,
    b'\xc3\xb9': TextCharacter.u_GRAVE,
    b'\xc3\xbf': TextCharacter.y_DIAERESIS,
    b'\xc3\x96': TextCharacter.O_DIAERESIS,
    b'\xc3\x9c': TextCharacter.U_DIAERESIS,
    b'\xc2\xa3': TextCharacter.POUNDS,
    b'\xc2\xa5': TextCharacter.YEN,
    b'\x25': TextCharacter.PERCENT,
    b'\xc6\x92': TextCharacter.FLORIN,
    b'\xc3\xad': TextCharacter.i_ACUTE,
    b'\xc3\xb3': TextCharacter.o_ACUTE,
    b'\xc3\xba': TextCharacter.u_ACUTE,
    b'\xc3\xb1': TextCharacter.n_TILDE,
    b'\xc3\x91': TextCharacter.N_TILDE,
    b'\xc2\xbf': TextCharacter.INVERT_QUESTION,
    b'\xc2\xb0': TextCharacter.DEGREES,
    b'\xc2\xa1': TextCharacter.INVERT_EXCLAIM,
    b'\xce\xb8': TextCharacter.theta,
    b'\xce\x98': TextCharacter.THETA,
    b'\xc4\x87': TextCharacter.c_ACUTE,
    b'\xC4\x86': TextCharacter.C_ACUTE,
    # assigning all betas to BETA b/c don't know what BETA2 actually is
    # TODO: change later
    b'\xcf\x90': TextCharacter.BETA,
    b'\xce\xb2': TextCharacter.BETA,
    b'\xce\x92': TextCharacter.BETA,
    b'\xc3\x81': TextCharacter.A_ACUTE,
    b'\xc3\x80': TextCharacter.A_GRAVE,
    b'\xc3\x8d': TextCharacter.I_ACUTE,
    b'\xc3\x95': TextCharacter.O_TILDE,
    b'\xc3\xb5': TextCharacter.o_TILDE
}
''' FOR ABOVE DICT ^
    Unsure what the difference is with these extra characters, will check
    the protocol spec and see later
    b'': TextCharacter.XC_C_CEDILLA,
    b'': TextCharacter.XC_u_DIAERESIS,
    b'': TextCharacter.XC_e_GRAVE,
    b'': TextCharacter.XC_a_CIRCUMFLEX,
    b'': TextCharacter.XC_a_DIAERESIS,
    b'': TextCharacter.XC_a_ACUTE,
    b'': TextCharacter.XC_a_RING_ABOVE,
    b'': TextCharacter.XC_c_CEDILLA,
    b'': TextCharacter.XC_e_CIRCUMFLEX,
    b'': TextCharacter.XC_e_DIAERESIS,
    b'': TextCharacter.XC_c_CEDILLA,
    b'': TextCharacter.XC_e_CIRCUMFLEX,
    b'': TextCharacter.XC_e_DIAERESIS,
    b'': TextCharacter.XC_i_DIAERESIS,
    b'': TextCharacter.XC_i_CIRCUMFLEX,
    b'': TextCharacter.XC_i_GRAVE,
    b'': TextCharacter.XC_A_DIAERESIS,
    b'': TextCharacter.XC_A_RING_ABOVE,
    b'': TextCharacter.XC_E_ACUTE,
    b'': TextCharacter.XC_ae_LIGATURE,
    b'': TextCharacter.XC_AE_LIGATURE,
    b'': TextCharacter.XC_o_CIRCUMFLEX,
    b'': TextCharacter.XC_o_DIAERESIS,
    b'': TextCharacter.XC_o_GRAVE,
    b'': TextCharacter.XC_u_CIRCUMFLEX,
    b'': TextCharacter.XC_u_GRAVE,
    b'': TextCharacter.XC_y_DIAERESIS,
    b'': TextCharacter.XC_O_DIAERESIS,
    b'': TextCharacter.XC_U_DIAERESIS,
    b'': TextCharacter.XC_CENTS,
    b'': TextCharacter.XC_POUNDS,
    b'': TextCharacter.XC_YEN,
    b'': TextCharacter.XC_PERCENT,
    b'': TextCharacter.XC_SLANT_F,
    b'': TextCharacter.XC_i_ACUTE,
    b'': TextCharacter.XC_o_ACUTE,
    b'': TextCharacter.XC_u_ACUTE,
    b'': TextCharacter.XC_n_TILDE,
    b'': TextCharacter.XC_N_TILDE,
    b'': TextCharacter.XC_SUPER_a,
    b'': TextCharacter.XC_SUPER_o,
    b'': TextCharacter.XC_INVERT_QUESTION,
    b'': TextCharacter.XC_DEGREES,
    b'': TextCharacter.XC_INVERT_EXCLAIM,
    b'': TextCharacter.XC_SINGLE_COL_SPACE,
    b'': TextCharacter.XC_theta,
    b'': TextCharacter.XC_THETA,
    b'': TextCharacter.XC_c_ACUTE,
    b'': TextCharacter.XC_C_ACUTE,
    b'': TextCharacter.XC_c,
    b'': TextCharacter.XC_C,
    b'': TextCharacter.XC_d,
    b'': TextCharacter.XC_D,
    b'': TextCharacter.XC_s,
    b'': TextCharacter.XC_z,
    b'': TextCharacter.XC_Z,
    b'': TextCharacter.XC_BETA,
    b'': TextCharacter.XC_S,
    b'': TextCharacter.XC_BETA2,
    b'': TextCharacter.XC_A_ACUTE,
    b'': TextCharacter.XC_A_GRAVE,
    b'': TextCharacter.XC_A_2ACUTE,
    b'': TextCharacter.XC_a_2ACUTE,
    b'': TextCharacter.XC_I_ACUTE,
    b'': TextCharacter.XC_O_TILDE,
    b'': TextCharacter.XC_o_TILDE,
    }
'''


class Animation:
    """
    Object designed to represent normal animations
    """
    @staticmethod
    def _validate_parameter(parameter: Union[str, bytes],
                            dictionary: Dict[str, bytes],
                            default_on_fail: Union[str, bytes]) -> Union[str, bytes]:
        """
        Validates the given parameter, defaulting to default_on_fail if the parameter is invalid
        :param parameter: parameter to validate
        :param dictionary: dictionary to validate parameter against
        :param default_on_fail: returned if given parameter is not valid
        """
        if parameter in dictionary.keys():
            return dictionary[parameter]
        elif parameter in dictionary.values():
            return parameter
        else:
            print(f"Invalid parameter provided to 'Animation' class constructor: parameter='{parameter}', "
                  f"defaulted to '{default_on_fail}'")
            return default_on_fail
    
    @staticmethod
    def generate_random():
        anim: Animation =  Animation("Random animation", None, None, None)
        anim.randomize()
        return anim

    def __init__(self,
                 text: str = "",
                 mode: Union[str, bytes] = TextMode.MODE_AUTO,
                 color: Union[str, bytes] = TextColor.TEXT_COLOR_AUTO,
                 position: Union[str, bytes] = TextPosition.TEXT_POS_MIDDLE) -> None:
        self.text = text
        self.mode: Union[str, bytes] = self._validate_parameter(mode, ANIMATION_MODE_DICT, TextMode.MODE_AUTO)
        self.color: Union[str, bytes] = self._validate_parameter(color, ANIMATION_COLOR_DICT,
                                                                 TextColor.TEXT_COLOR_AUTO)
        self.position: Union[str, bytes] = self._validate_parameter(position, ANIMATION_POS_DICT,
                                                                    TextPosition.TEXT_POS_MIDDLE)

    def __str__(self) -> str:
        """
        String representation of this Animation
        :return: a string representation of this Animation
        """
        return f"Animation: text='{self.text}' mode={self.mode} color={self.color} position={self.position}"

    def __repr__(self) -> str:
        return self.__str__()

    def reset(self) -> None:
        self.text: str = ""
        self.mode: bytes = TextMode.MODE_AUTO
        self.color: bytes = TextColor.TEXT_COLOR_AUTO
        self.position: bytes = TextPosition.TEXT_POS_MIDDLE

    def randomize(self) -> None:
        self.mode: bytes = random.choice(list(ANIMATION_MODE_DICT.values()))
        self.color: bytes = random.choice(list(ANIMATION_COLOR_DICT.values()))
        self.position: bytes = random.choice(list(ANIMATION_POS_DICT.values()))

    def display(self, files: bytes = FileName.FILE_PRIORITY) -> None:
        """
        Sends this animation straight to the display
        """
        _transmit(_write_file(self, file=file))

    def bytestr(self) -> bytes:
        """
        Returns the bytestring representation of this Animation (along with the necessary start of mode
        character)
        """
        return PacketCharacter.SOM + self.position + self.mode + self.color + _transcode(self.text)


def _transmit(payload: bytes, addr: bytes = SignAddress.SIGN_ADDRESS_BROADCAST,
              ttype: bytes = SignType.SIGN_TYPE_ALL_VERIFY, port: str = SERIAL_PORT) -> None:
    """
    Transmits a single packet
    :param payload: packet Command Code + Data Field to transmit
    :param addr: packet Sign Address - the address of the sign. See the protocol write-up summary for more details.
    :param ttype: packet Type Code - describes the type of sign we're communicating to
    :return: None
    """
    packet: bytes = (PacketCharacter.WAKEUP + PacketCharacter.SOH + ttype + addr + PacketCharacter.STX + payload +
                     PacketCharacter.EOT)
    ser: Serial = Serial(port, 9600, timeout=10)
    ser.write(packet)
    ser.close()


def _transmit_multi(payloads: List[bytes], addr: bytes = SignAddress.SIGN_ADDRESS_BROADCAST,
                    ttype: bytes = SignType.SIGN_TYPE_ALL_VERIFY) -> None:
    """
    [UNTESTED]
    Transmits multiple packets (in nested packet format, as per 5.1.3 in the specification)
    :param payloads: packet Command Code + Data Field to transmit, as a list, where each item is the combined bytestring
    of each Command Code and Data Field pair
    :param addr: packet Sign Address - the address of the sign. See the protocol write-up summary for more details.
    :param ttype: packet Type Code - describes the type of sign we're communicating to
    :return: None
    """
    # This would be a cool one liner to form the packet BUT we need to have 100ms delays after <STX>'s
    # packet = WAKEUP + SOH + ttype + addr + STX + (ETX+STX).join(payloads) + ETX + EOT
    ser: Serial = Serial(SERIAL_PORT, 9600, timeout=10)
    # Initial wakeup
    ser.write(PacketCharacter.WAKEUP + PacketCharacter.SOH + ttype + addr)
    for payload in payloads:
        ser.write(PacketCharacter.STX)
        # 100ms wait + python's performance delay should be adequate here
        time.sleep(.1)
        ser.write(payload + PacketCharacter.ETX)
    # Signal end of packet transmission
    ser.write(PacketCharacter.EOT)
    ser.close()


def _receive(timeout: int = 10) -> bytes:
    """
    Receives data from the serial sign (until reaching an EOT)
    :param timeout: time to receive until we timeout
    """
    ser: Serial = Serial(SERIAL_PORT, 9600, timeout=timeout)
    received: bytes = ser.read_until(PacketCharacter.EOT)
    return received


def _write_file(animations: Union[List[Animation], Animation], file: bytes = FileName.FILE_PRIORITY) -> bytes:
    """Writes the given animations (which could be a single animation) in the proper payload format
    If file is anything but FILE_PRIORITY, then memory needs to be allocated and dealt with before hand
    Maybe I'll add a memory configuration function that assigns memory per some sort of input specification
    :param animations:
    :param file:
    :return:
    """
    #   Many animations
    if isinstance(animations, list):
        payload: bytes = CommandCode.COMMAND_WRITE_TEXT + file
        for x in range(len(animations)):
            animation: Animation = animations.pop(0)
            payload += animation.bytestr()
    #   One animation
    elif isinstance(animations, Animation):
        payload: bytes = CommandCode.COMMAND_WRITE_TEXT + file + animations.bytestr()
    else:
        raise ValueError(f"Invalid argument given: animations='{animations}'")
    return payload


def send_dots(dots_data: bytes, width: Optional[Union[int, bytes]] = None, height: Optional[Union[int, bytes]] = None,
              file: FileName = FileName.FILE_PRIORITY) -> None:
    """
    [UNTESTED]
    Sends a SMALL DOTS PICTURE file to the sign, as per 6.4.1 in the specification
    dots_data should be formatted as such:
    2 hex bytes for height + 2 hex bytes for width + row bit pattern + carriage return
    :param file: File label to write to
    :param dots_data: DOTS data to transmit
    :param width: width of DOTS image
    :param height: height of DOTS image
    :return: None
    """
    if width is None:
        width: int = len(max(str(dots_data).split('\r')))
    if height is None:
        height: int = len(str(dots_data).split('\r'))
    if isinstance(width, int):
        width: bytes = width.to_bytes(2, "big")
    if isinstance(height, int):
        height: bytes = height.to_bytes(2, "big")
    _transmit(CommandCode.COMMAND_WRITE_DOTS + file + height + width + dots_data + TextCharacter.CR)


def _transcode(msg: str) -> bytes:
    """
    Transcodes the given msg to an appropriate bytes representation, needs to be expanded to account for all available
    characters
    :param msg: string to transcode
    :return: the msg's bytes representation
    """
    transcoded: bytes = b''
    for char in msg:
        b: bytes = bytes(char, 'utf-8')
        transcoded += TextCharacterTranslationDict[b] if b in TextCharacterTranslationDict else b
    return transcoded


def set_time() -> None:
    """
    [UNTESTED]
    Sets the time of day (in 24-hour format) in the sign, in the format HhMm
    :return: None
    """
    _transmit(CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.SET_TIME_OF_DAY + bytes(
        datetime.now().strftime("%H%M"), 'utf-8'))


def soft_reset() -> None:
    _transmit(CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.SOFT_RESET)


def send_animations(animations: Union[Animation, List[Animation]]) -> None:
    """
    Transmits the given list of animations to the betabrite sign
    :param animations: list of animations to transmit
    :return: None
    """
    #   If you want to send just one animation, you can use its 'display()' method
    # _transmit(SERIAL_PORT, _write_file(animations, file=FILE_NORMAL_RANGE[0]))
    # To transmit to a non
    _transmit(_write_file(animations, file=FileName.FILE_PRIORITY))


def _cli_parse_animations_from_string(animation_string: str) -> List[Animation]:
    """
    animation_string should be formatted as such:
    TEXT ANIMATION_MODE ANIMATION_COLOR ANIMATION_POSITION$CLI_TERMINAL_AND$NEXT_ANIMATION
    e.g. chungus cherrybomb rainbow2 None-bingus None amber None
    where '-' is replaced with the CLI_TERMINAL_AND
    """
    return _cli_parse_animations(animation_string.split(CLI_TERMINAL_AND))


def _cli_parse_animations(animations: List[str]):
    parsed_animations: List[Animation] = []
    while len(animations) != 0:
        animget: List[Union[str, bytes]] = animations.pop(0).split(CLI_ANIMATION_PROPERTY_SEPARATOR)
        animget[0]: str = animget[0] if animget[0] != "None" else ""
        animget[1]: Union[str, bytes] = ANIMATION_MODE_DICT[animget[1]] if animget[1] != "None" \
            else TextMode.MODE_AUTO
        animget[2]: Union[str, bytes] = ANIMATION_COLOR_DICT[animget[2]] if animget[2] != "None" \
            else TextColor.TEXT_COLOR_AUTO
        animget[3]: Union[str, bytes] = ANIMATION_POS_DICT[animget[3]] if animget[3] != "None" \
            else TextPosition.TEXT_POS_MIDDLE
        parsed_animations.append(Animation(animget[0], animget[1], animget[2], animget[3]))

    return parsed_animations


def read_general_information() -> bytes:
    """
    Reads general information bytes from the sign and returns it
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.READ_GENERAL_INFORMATION)
    return _receive()


def main() -> None:
    # pylint: disable=import-outside-toplevel
    import argparse
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "messages",
        help=f"messages to send, structured like: \n"
             f"TEXT,ANIMATION_MODE,ANIMATION_COLOR,ANIMATION_POSITION{CLI_TERMINAL_AND}[next message or EOL]",
        nargs='+')
    args: argparse.Namespace = parser.parse_args()
    # display_DOTS(None)
    animations: str = ' '.join(args.messages)
    animations: List[Animation] = _cli_parse_animations_from_string(animations)
    if CLI_ALLOW_TRANSMISSION:
        _transmit(_write_file(animations))
    else:
        print(f"Packet: {animations}")
        print(f"Write_file: {_write_file(animations)}")


if __name__ == '__main__':
    main()
