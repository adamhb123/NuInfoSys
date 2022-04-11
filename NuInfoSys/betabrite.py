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
import random
from datetime import datetime
from typing import Union, List, Dict, Optional
from serial import Serial

from NuInfoSys import config
# pylint: disable=wildcard-import
from NuInfoSys.framecontrolbytes import *
from NuInfoSys import memory

# Note that on the BetaBrite, position does not matter at all, so setting any of these does nothing
# IT IS still required to be sent in the message packet, however
ANIMATION_POS_DICT: Dict[str, bytes] = {
    'middle': TextPosition.MIDDLE,
    'top': TextPosition.TOP,
    'bottom': TextPosition.BOTTOM,
    'fill': TextPosition.FILL
}

ANIMATION_COLOR_DICT: Dict[str, bytes] = {
    'red': TextColor.RED,
    'green': TextColor.GREEN,
    'amber': TextColor.AMBER,
    'dimred': TextColor.DIMRED,
    'brown': TextColor.BROWN,
    'orange': TextColor.ORANGE,
    'yellow': TextColor.YELLOW,
    'rainbow1': TextColor.RAINBOW1,
    'rainbow2': TextColor.RAINBOW2,
    'mix': TextColor.MIX,
    'autocolor': TextColor.AUTO
}

ANIMATION_MODE_DICT: Dict[str, bytes] = {
    'rotate': TextMode.ROTATE,
    'hold': TextMode.HOLD,
    'flash': TextMode.FLASH,
    'rollup': TextMode.ROLLUP,
    'rolldown': TextMode.ROLLDOWN,
    'rollleft': TextMode.ROLLLEFT,
    'rollright': TextMode.ROLLRIGHT,
    'wipeup': TextMode.WIPEUP,
    'wipedown': TextMode.WIPEDOWN,
    'wipeleft': TextMode.WIPELEFT,
    'wiperight': TextMode.WIPERIGHT,
    'scroll': TextMode.SCROLL,
    'automode': TextMode.AUTO,
    'rollin': TextMode.ROLLIN,
    'rollout': TextMode.ROLLOUT,
    'wipein': TextMode.WIPEIN,
    'wipeout': TextMode.WIPEOUT,
    'cmprsrot': TextMode.CMPRSROT,
    'twinkle': TextMode.TWINKLE,
    'sparkle': TextMode.SPARKLE,
    'snow': TextMode.SNOW,
    'interlock': TextMode.INTERLOCK,
    'switch': TextMode.SWITCH,
    'spray': TextMode.SPRAY,
    'starburst': TextMode.STARBURST,
    'welcome': TextMode.WELCOME,
    'slotmachine': TextMode.SLOTMACHINE,
    'newsflash': TextMode.NEWSFLASH,
    'trumpet': TextMode.TRUMPET,
    'thankyou': TextMode.THANKYOU,
    'nosmoking': TextMode.NOSMOKING,
    'drinkdrive': TextMode.DRINKDRIVE,
    'animal': TextMode.ANIMAL,
    'fish': TextMode.FISH,
    'fireworks': TextMode.FIREWORKS,
    'turbocar': TextMode.TURBOCAR,
    'balloons': TextMode.BALLOONS,
    'cherrybomb': TextMode.CHERRYBOMB
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
    def generate_random() -> 'Animation':
        anim: Animation = Animation("Random animation", None, None, None)
        anim.randomize()
        return anim

    @staticmethod
    def _validate_parameter(parameter: Optional[Union[str, bytes]],
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
            if parameter is not None:
                print(f"Invalid parameter provided to 'Animation' class constructor: parameter='{parameter}', "
                      f"defaulted to '{default_on_fail}'")
            return default_on_fail

    def __init__(self,
                 text: str = "",
                 mode: Optional[Union[str, bytes]] = TextMode.AUTO,
                 color: Optional[Union[str, bytes]] = TextColor.AUTO,
                 position: Optional[Union[str, bytes]] = TextPosition.MIDDLE) -> None:
        self.text = text
        self.mode: Union[str, bytes] = self._validate_parameter(mode, ANIMATION_MODE_DICT, TextMode.AUTO)
        self.color: Union[str, bytes] = self._validate_parameter(color, ANIMATION_COLOR_DICT,
                                                                 TextColor.AUTO)
        self.position: Union[str, bytes] = self._validate_parameter(position, ANIMATION_POS_DICT,
                                                                    TextPosition.MIDDLE)

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
        self.mode: bytes = TextMode.AUTO
        self.color: bytes = TextColor.AUTO
        self.position: bytes = TextPosition.MIDDLE

    def randomize(self) -> None:
        self.mode: bytes = random.choice(list(ANIMATION_MODE_DICT.values()))
        self.color: bytes = random.choice(list(ANIMATION_COLOR_DICT.values()))
        self.position: bytes = random.choice(list(ANIMATION_POS_DICT.values()))

    def display(self, file: bytes = FileName.FILE_PRIORITY) -> bytes:
        """
        Sends this animation straight ta the display

        :return: Bytes representing the sent packet
        """
        return _transmit(_write_file(self, file=file))

    def bytes(self) -> bytes:
        """
        Returns the bytestring representation of this Animation's transmission packet (along with the necessary start
        of mode character)
        """
        return PacketCharacter.SOM + self.position + self.mode + self.color + _transcode(self.text)

    def ascii(self):
        """
        Returns the ASCII representation of this Animation's trans (along with the necessary start of mode
        character)
        """
        return PacketCharacter.SOM.decode("ascii") + self.position.decode("ascii") + self.mode.decode(
            "ascii") + self.color.decode("ascii") + _transcode(self.text).decode("ascii")


'''
[UTILITY]
Utility Methods
'''


def _transmit(payload: bytes, addr: bytes = SignAddress.SIGN_ADDRESS_BROADCAST,
              ttype: bytes = SignType.SIGN_TYPE_ALL_VERIFY, port: str = config.SERIAL_PORT) -> bytes:
    """
    Transmits a single packet
    :param payload: packet Command Code + Data Field to transmit
    :param addr: packet Sign Address - the address of the sign. See the protocol write-up summary for more details.
    :param ttype: packet Type Code - describes the type of sign we're communicating to
    :return: Bytes representing the sent packet
    """
    packet: bytes = (PacketCharacter.WAKEUP + PacketCharacter.SOH + ttype + addr + PacketCharacter.STX + payload +
                     PacketCharacter.EOT)
    ser: Serial = Serial(port, config.BAUD_RATE, timeout=10)
    ser.write(packet)
    ser.close()
    return packet


def _transmit_multi(payloads: List[bytes], addr: bytes = SignAddress.SIGN_ADDRESS_BROADCAST,
                    ttype: bytes = SignType.SIGN_TYPE_ALL_VERIFY) -> bytes:
    """
    [UNTESTED]
    Transmits multiple packets (in nested packet format, as per 5.1.3 in the specification)
    :param payloads: packet Command Code + Data Field to transmit, as a list, where each item is the combined bytestring
    of each Command Code and Data Field pair
    :param addr: packet Sign Address - the address of the sign. See the protocol write-up summary for more details.
    :param ttype: packet Type Code - describes the type of sign we're communicating to
    :return: Bytes representing the sent packet (containing all nested packets)
    """
    # This would be a cool one liner to form the packet BUT we need to have 100ms delays after <STX>'s
    # packet = WAKEUP + SOH + ttype + addr + STX + (ETX+STX).join(payloads) + ETX + EOT
    ser: Serial = Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=10)
    # Initial wakeup
    # final_packet only exists here so that we can return what we've sent to serial
    final_packet: bytes = PacketCharacter.WAKEUP + PacketCharacter.SOH + ttype + addr
    ser.write(final_packet)
    for payload in payloads:
        ser.write(PacketCharacter.STX)
        final_packet += PacketCharacter.STX
        # 100ms wait + python's performance delay should be adequate here
        time.sleep(.1)
        ser.write(payload + PacketCharacter.ETX)
        final_packet += payload + PacketCharacter.ETX
    # Signal end of packet transmission
    ser.write(PacketCharacter.EOT)
    final_packet += PacketCharacter.EOT
    ser.close()
    return final_packet


def _receive(timeout: int = 10) -> bytes:
    """
    Receives data from the serial sign (until reaching an EOT)
    :param timeout: time to receive until we timeout
    """
    ser: Serial = Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=timeout)
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
            payload += animation.bytes()
    #   One animation
    elif isinstance(animations, Animation):
        payload: bytes = CommandCode.COMMAND_WRITE_TEXT + file + animations.bytes()
    else:
        raise ValueError(f"Invalid argument given: animations='{animations}'")
    return payload


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


'''
[CLI]
CLI Methods
'''


def _cli_parse_animations_from_string(animation_string: str) -> List[Animation]:
    """
    animation_string should be formatted as such:
    TEXT ANIMATION_MODE ANIMATION_COLOR ANIMATION_POSITION$config.CLI_TERMINAL_AND$NEXT_ANIMATION
    e.g. chungus cherrybomb rainbow2 None-bingus None amber None
    where '-' is replaced with the config.CLI_TERMINAL_AND
    """
    return _cli_parse_animations(animation_string.split(config.CLI_TERMINAL_AND))


def _cli_parse_animations(animations: List[str]):
    parsed_animations: List[Animation] = []
    while len(animations) != 0:
        animget: List[Union[str, bytes]] = animations.pop(0).split(config.CLI_ANIMATION_PROPERTY_SEPARATOR)
        animget[0]: str = animget[0] if animget[0] != "None" else ""
        animget[1]: Union[str, bytes] = ANIMATION_MODE_DICT[animget[1]] if animget[1] != "None" \
            else TextMode.AUTO
        animget[2]: Union[str, bytes] = ANIMATION_COLOR_DICT[animget[2]] if animget[2] != "None" \
            else TextColor.AUTO
        animget[3]: Union[str, bytes] = ANIMATION_POS_DICT[animget[3]] if animget[3] != "None" \
            else TextPosition.MIDDLE
        parsed_animations.append(Animation(animget[0], animget[1], animget[2], animget[3]))

    return parsed_animations


'''
[SIGN IO]
Send Methods
'''


def send_dots(dots_data: bytes, width: Optional[Union[int, bytes]] = None,
              height: Optional[Union[int, bytes]] = None,
              file: bytes = FileName.FILE_PRIORITY) -> bytes:
    """
    [UNTESTED]
    Sends a SMALL DOTS PICTURE file to the sign, as per 6.4.1 in the specification
    dots_data should be formatted as such:
    2 hex bytes for height + 2 hex bytes for width + row bit pattern + carriage return
    :param file: File label to write to
    :param dots_data: DOTS data to transmit
    :param width: width of DOTS image
    :param height: height of DOTS image
    :return: Bytes sent in packet
    """
    if width is None:
        width: int = len(max(str(dots_data).split('\r')))
    if height is None:
        height: int = len(str(dots_data).split('\r'))
    if isinstance(width, int):
        width: bytes = width.to_bytes(1, "big")
    if isinstance(height, int):
        height: bytes = height.to_bytes(1, "big")
    dots_data.replace(b"\r", TextCharacter.CR)
    packet: bytes = CommandCode.COMMAND_WRITE_DOTS + file + height + width + dots_data
    return _transmit(packet)


def send_time() -> bytes:
    """
    [UNTESTED]
    Sends the time of day (in 24-hour format) to the sign, in the format HhMm

    :return: Bytes sent in packet
    """
    packet: bytes = CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.SET_TIME_OF_DAY + bytes(
        datetime.now().strftime("%H%M"), 'utf-8')

    return _transmit(packet)


def send_soft_reset() -> bytes:
    """
    [TESTED]
    Sends the soft reset command to the sign

    :return: Bytes sent in packet
    """
    packet: bytes = CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.SOFT_RESET

    return _transmit(packet)


def send_set_large_dots_picture_memory_configuration_single(filename: Union[str, bytes], width: Union[int, bytes],
                                                            height: Union[int, bytes]) -> bytes:
    """
    [UNTESTED]
    Sends...

    :return: Bytes sent in packet
    """
    if isinstance(filename, str):
        filename: bytes = bytes(filename, "utf-8")
    if len(filename) < 9:
        filename += b' ' * (9 - len(filename))
    elif len(filename) > 9:
        raise ValueError(
            "Invalid filename provided to send_set_large_dots_picture_memory_configuration: filename too long")
    if isinstance(width, int):
        width: bytes = width.to_bytes(2, 'big')
    if isinstance(height, int):
        height: bytes = height.to_bytes(2, 'big')

    packet: bytes = CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.SET_LARGE_DOTS_PICTURE_MEMORY_CONFIGURATION + filename + height + width + b"0000"
    return _transmit(packet)


def send_set_large_dots_picture_memory_configuration_all() -> bytes:
    """
    [UNTESTED, UNFINISHED]
    Sends...

    :return: Bytes sent in packet
    """
    for fn in FileName:  # type: ignore
        # send_set_large_dots_picture_memory_configuration_single(fn.name[:9], )
        pass
    return b''


def send_animations(animations: Union[Animation, List[Animation]], file: bytes = FileName.FILE_PRIORITY,
                    addr: bytes = SignAddress.SIGN_ADDRESS_BROADCAST,
                    ttype: bytes = SignType.SIGN_TYPE_ALL_VERIFY) -> bytes:
    """
    Transmits the given list of animations to the betabrite sign
    :param animations: list of animations to transmit
    :param file: file to send animations to
    :param addr: sign address
    :param ttype: sign type

    :return: Bytes sent in packet
    """
    #   If you want to send just one animation, you can use its 'display()' method
    # _transmit(config.SERIAL_PORT, _write_file(animations, file=FILE_NORMAL_RANGE[0]))
    packet: bytes = _write_file(animations, file=file)
    return _transmit(packet, addr=addr, ttype=ttype)


'''
[SIGN IO]
Read Methods - will have to add plain english translation
'''


def read_time() -> bytes:
    """
    [UNTESTED]
    Reads time bytes from the sign

    :return: Time bytes read from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.TIME_OF_DAY)
    return _receive()


def read_speaker_status() -> bytes:
    """
    [UNTESTED]
    Reads speaker status from the sign

    :return: speaker status bytes read from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.SPEAKER_STATUS)
    return _receive()


def read_general_information() -> bytes:
    """
    [TESTED]
    Reads general information bytes from the sign
    :return: General information bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.GENERAL_INFORMATION)
    return _receive()


def read_memory_pool_size() -> bytes:
    """
    [UNTESTED]
    Reads memory pool size bytes from the sign
    :return: Memory pool size bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.MEMORY_POOL_SIZE)
    return _receive()


def read_memory_configuration() -> bytes:
    """
    [UNTESTED]
    Reads memory configuration bytes from the sign
    :return: Memory configuration bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.MEMORY_CONFIGURATION)
    return _receive()


def read_memory_dump() -> bytes:
    """
    [UNTESTED]
    Reads memory dump bytes from the sign
    :return: Memory dump bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.MEMORY_DUMP)
    return _receive()


def read_day_of_week() -> bytes:
    """
    [UNTESTED]
    Reads day of week bytes from the sign
    :return: Day of week bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.DAY_OF_WEEK)
    return _receive()


def read_time_format() -> bytes:
    """
    [UNTESTED]
    Reads time format bytes from the sign
    :return: Time format bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.TIME_FORMAT)
    return _receive()


def read_run_time_table() -> bytes:
    """
    [UNTESTED]
    Reads run time table bytes from the sign
    :return: Run time table bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.RUN_TIME_TABLE)
    return _receive()


def read_serial_error_status_register() -> bytes:
    """
    [UNTESTED]
    Reads serial error status register table bytes from the sign
    :return: Serial error status register from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.SERIAL_ERROR_STATUS_REGISTER)
    return _receive()


def read_network_query() -> bytes:
    """
    [UNTESTED]
    Reads network query bytes from the sign
    :return: Network query from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.NETWORK_QUERY)
    return _receive()


def read_run_sequence() -> bytes:
    """
    [UNTESTED]
    Reads serial error status register table bytes from the sign
    :return: Serial error status register from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.RUN_SEQUENCE)
    return _receive()


def read_run_day_table() -> bytes:
    """
    [UNTESTED]
    Reads run day table bytes from the sign
    :return: Run day table from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.RUN_DAY_TABLE)
    return _receive()


def read_counter() -> bytes:
    """
    [UNTESTED]
    Reads counter bytes from the sign
    :return: Counter bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.COUNTER)
    return _receive()


def read_large_dots_picture_memory_configuration() -> bytes:
    """
    [UNTESTED]
    Reads large dots picture memory configuration bytes from the sign
    :return: Large dots picture memory configuration bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.LARGE_DOTS_PICTURE_MEMORY_CONFIGURATION)
    return _receive()


def read_date() -> bytes:
    """
    [UNTESTED]
    Reads date bytes from the sign
    :return: Date bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.LARGE_DOTS_PICTURE_MEMORY_CONFIGURATION)
    return _receive()


def read_temperature_offset() -> bytes:
    """
    [UNTESTED]
    Reads temperature offset bytes from the sign
    :return: Temperature offset bytes from the sign
    """
    _transmit(CommandCode.COMMAND_READ_SPECIAL + ReadSpecialFunctionLabel.TEMPERATURE_OFFSET)
    return _receive()


def main() -> None:
    """
    CLI Entrypoint
    """
    # pylint: disable=import-outside-toplevel
    import argparse
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "messages",
        help=f"messages to send, structured like: \n"
             f"TEXT,ANIMATION_MODE,ANIMATION_COLOR,ANIMATION_POSITION{config.CLI_TERMINAL_AND}[next message or EOL]",
        nargs='+')
    args: argparse.Namespace = parser.parse_args()
    # display_DOTS(None)
    animations: str = ' '.join(args.messages)
    animations: List[Animation] = _cli_parse_animations_from_string(animations)
    if config.CLI_ALLOW_TRANSMISSION:
        _transmit(_write_file(animations))
    else:
        print(f"CLI transmission is disabled...")
        print(f"Packets (bytes): {[x.bytes() for x in animations]}")
        print(f"Packets (ASCII): {[x.ascii() for x in animations]}")


if __name__ == '__main__':
    main()
