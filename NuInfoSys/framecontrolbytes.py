"""Contains Frame Control Bytes used for communication with BetaBrite

Currently, some of the characters need to be reverified
"""
'''
A note on memory (from the protocol specification):
"The sum of all the file sizes (except for SMALL DOTS PICTURE and LARGE DOTS PICTURE files) plus 11 bytes of overhead
for each file should not exceed the total amount of available memory in the pool. A value of “0000” is a valid SIZE for
the last file in the Memory Configuration only if this last file is a TEXT file. This assigns all remaining memory to
the file."

'''
from enum import Enum
from typing import Any


class _GetterEnum(Enum):
    def __get__(self, instance: Any, owner: Any) -> Any:
        return self.value


TOTAL_MEMORY: int = 30000


class SignType(_GetterEnum):
    SIGN_TYPE_ALL_VERIFY: bytes = b"!"
    SIGN_TYPE_SERIAL_CLOCK: bytes = b"\""  # serial clock
    SIGN_TYPE_ALPHAVISION: bytes = b"#"  # alphavision
    SIGN_TYPE_ALPHAVISION_FULL: bytes = b"$"  # full matrix alphavision
    SIGN_TYPE_ALPHAVISION_CHAR: bytes = b"%"  # character matrix alphavision
    SIGN_TYPE_ALPHAVISION_LINE: bytes = b"&"  # line matrix alphavision
    SIGN_TYPE_RESPONSE: bytes = b"0"  # sign response
    SIGN_TYPE_ONE_LINE: bytes = b"1"  # one line signs
    SIGN_TYPE_TWO_LINE: bytes = b"2"  # two line signs
    SIGN_TYPE_430I: bytes = b"C"  # 430i
    SIGN_TYPE_440I: bytes = b"D"  # 440i
    SIGN_TYPE_460I: bytes = b"E"  # 460i
    SIGN_TYPE_790I: bytes = b"U"  # 790i
    SIGN_TYPE_ALL: bytes = b"Z"  # all signs
    SIGN_TYPE_BETABRITE: bytes = b"^"  # betabrite
    SIGN_TYPE_4120C: bytes = b"a"  # 4120c
    SIGN_TYPE_4160C: bytes = b"b"  # 4160c
    SIGN_TYPE_4200C: bytes = b"c"  # 4200c
    SIGN_TYPE_4240C: bytes = b"d"  # 4240c
    SIGN_TYPE_215: bytes = b"e"  # 215
    SIGN_TYPE_215C: bytes = b"f"  # 215c
    SIGN_TYPE_4120R: bytes = b"g"  # 4120r
    SIGN_TYPE_4160R: bytes = b"h"  # 4160r
    SIGN_TYPE_4200R: bytes = b"i"  # 4200r
    SIGN_TYPE_4240R: bytes = b"j"  # 4240r
    SIGN_TYPE_300: bytes = b"k"  # 300
    SIGN_TYPE_7000: bytes = b"l"  # 7000
    SIGN_TYPE_SOLAR_96X16: bytes = b"m"  # solar 96x16 matrix
    SIGN_TYPE_SOLAR_128X16: bytes = b"n"  # solar 128x16 matrix
    SIGN_TYPE_SOLAR_160X16: bytes = b"o"  # solar 160x16 matrix
    SIGN_TYPE_SOLAR_192X16: bytes = b"p"  # solar 192x16 matrix
    SIGN_TYPE_SOLAR_PPD: bytes = b"q"  # ppd
    SIGN_TYPE_DIRECTOR: bytes = b"r"  # director
    SIGN_TYPE_4080C: bytes = b"t"  # 4080c
    SIGN_TYPE_2X0C: bytes = b"u"  # 210c and 220c
    SIGN_TYPE_ALL_CONFIG: bytes = b"z"  # all signs


class CommandCode(_GetterEnum):
    COMMAND_WRITE_TEXT: bytes = b"A"  # write TEXT file
    COMMAND_READ_TEXT: bytes = b"B"  # read TEXT file
    COMMAND_WRITE_SPECIAL: bytes = b"E"  # write SPECIAL function
    COMMAND_READ_SPECIAL: bytes = b"F"  # read SPECIAL function
    COMMAND_WRITE_STRING: bytes = b"G"  # write STRING file
    COMMAND_READ_STRING: bytes = b"H"  # read STRING file
    COMMAND_WRITE_DOTS: bytes = b"I"  # write DOTS picture
    COMMAND_READ_DOTS: bytes = b"J"  # read DOTS picture
    COMMAND_WRITE_ALPHA_DOTS: bytes = b"M"  # write ALPHAVISION DOTS picture
    COMMAND_READ_ALPHA_DOTS: bytes = b"N"  # read ALPHAVISION DOTS picture
    COMMAND_ALPHA_BULLETIN: bytes = b"O"  # write ALPHAVISION BULLETIN


'''
Sound:
    1) NEVER use b"A" or b"B" to turn the sign's speaker on or off, as this can damage the sign (I have no idea why,
    the protocol reference just said so). Use the above (ENABLE_SPEAKER, DISABLE_SPEAKER) instead.
    2) Wait a minimum of 3 seconds before transmitting more data to the sign after sound generation
    3) Note that when a tone is generated, the sign's serial port is disabled until the tone is finished, which is the
    reasoning for the above
    4) When sending nested frames, the tone generation command must always come last, as the serial connection is
    temporarily disabled after the tone is generated (meaning the rest of the packet won't send)

'''

'''
Modifying memory:
    CLEAR MEMORY: just send E$ (with appropriate surroundings for packet formatting, see 6.2.1 table 15)
    SET MEMORY: REQUIRED for writing to files besides the priority file. See 6.2.1 table 15. Memory configuration
    uses the following format: FTPSIZEQQQQ, where F is 1 ASCII char representing the file label, T is 1 ASCII char
    representing the file type
'''


class WriteSpecialFunctionsLabel(_GetterEnum):
    """
    Write special functions labels, see 6.2.1 table 15 for details
    """
    SET_TIME_OF_DAY: bytes = b" "  # Set time of day
    ENABLE_SIGN_SPEAKER: bytes = b"00"  # Enable sign's speaker
    DISABLE_SIGN_SPEAKER: bytes = b"FF"  # Disable sign's speaker
    MODIFY_MEMORY: bytes = b"$"  # Modify memory, see 6.2.1 Table 15 and 'Modifying memory' above for details
    SET_DAY_OF_WEEK: bytes = b"&"  # Set the current day of the week
    SET_TIME_FORMAT: bytes = b"'"
    GENERATE_SPEAKER_TONE: bytes = b"("
    DISPLAY_TEXT_AT_XY_POSITION: bytes = b"+"
    SET_RUN_TIME_TABLE: bytes = b')'  # Sets the time that a text file will run at
    SOFT_RESET: bytes = b","
    SET_RUN_SEQUENCE: bytes = b'.'  # Specifies the run sequence for text files
    SET_RUN_DAY_TABLE: bytes = b'2'  # Sets the day that a text file will run on
    CLEAR_SERIAL_ERROR_STATUS_REGISTER: bytes = b"4"
    SET_COUNTER: bytes = b"5"  # I don't believe the BetaBrite has a counter, but am including this just in case
    # ^ check out 6.2.1 table 15 - "Set Counter" for details
    SET_SERIAL_ADDRESS: bytes = b"7"
    SET_LARGE_DOTS_PICTURE_MEMORY_CONFIGURATION: bytes = b"8"
    APPEND_TO_LARGE_DOTS_PICTURE_FILE_MEMORY_CONFIGURATION: bytes = b"9"


class DateTime(_GetterEnum):
    """
    All constants relevant to dates/times/schedules
    Contains constants used by SET_DAY_OF_WEEK, SET_RUN_DAY_TABLE,
    Contains constants returned by READ_DAY_OF_WEEK, READ_RUN_DAY_TABLE
    """
    DAILY: bytes = b"0"
    SUNDAY: bytes = b"1"
    MONDAY: bytes = b"2"
    TUESDAY: bytes = b"3"
    WEDNESDAY: bytes = b"4"
    THURSDAY: bytes = b"5"
    FRIDAY: bytes = b"6"
    SATURDAY: bytes = b"7"
    MONDAY_THROUGH_FRIDAY: bytes = b"8"
    WEEKENDS: bytes = b"9"
    ALWAYS: bytes = b"A"
    NEVER: bytes = b"B"
    STANDARD_AM_PM_FORMAT: bytes = b"S"
    TWENTY_FOUR_HOUR_MILITARY_TIME: bytes = b"M"


class Speaker(_GetterEnum):
    """
    All constants relevant to the speaker that are not listed elsewhere
    """
    pass


class FileType(_GetterEnum):
    """
    File types
    Contains constants used by SET_MEMORY_CONFIGURATION
    Contains constants returned by READ_MEMORY_CONFIGURATION
    """
    TEXT: bytes = b"A"
    STRING: bytes = b"B"
    DOTS: bytes = b"D"


class FileLock(_GetterEnum):
    """
    File lock indicators, used in READ & WRITE SPECIAL FUNCTION commands
    """
    UNLOCKED: bytes = b"U"
    LOCKED: bytes = b"L"


class TextFileTime(_GetterEnum):
    """
    Might change this later TODO: guh
    """
    ALLDAY: bytes = b"FD"
    NEVER: bytes = b"FE"
    ALWAYS: bytes = b"FF"


class DOTSColorStatus(_GetterEnum):
    # TODO: don't know if these should be like b"1000" or b"\x10\x00", assume the former b/c the protocol doesn't
    # TODO: follow them with 'H'
    MONOCHROME: bytes = b"1000"
    THREE_COLOR: bytes = b"2000"
    EIGHT_COLOR: bytes = b"4000"


class ReadSpecialFunctionLabel(_GetterEnum):
    TIME_OF_DAY: bytes = b" "
    SPEAKER_STATUS: bytes = b"!"
    GENERAL_INFORMATION: bytes = b"\""
    MEMORY_POOL_SIZE: bytes = b"#"
    MEMORY_CONFIGURATION: bytes = b"$"
    MEMORY_DUMP: bytes = b"%"
    DAY_OF_WEEK: bytes = b"&"
    TIME_FORMAT: bytes = b"'"
    RUN_TIME_TABLE: bytes = b")"
    SERIAL_ERROR_STATUS_REGISTER: bytes = b"*"
    NETWORK_QUERY: bytes = b"-"
    RUN_SEQUENCE: bytes = b"."
    RUN_DAY_TABLE: bytes = b"2"
    COUNTER: bytes = b"5"
    LARGE_DOTS_PICTURE_MEMORY_CONFIGURATION = b"8"
    DATE = b";"
    TEMPERATURE_OFFSET = b"T"


class FileName(_GetterEnum):
    FILE_1 = b' '
    FILE_2 = b'!'
    FILE_3 = b'"'
    FILE_4 = b'#'
    FILE_5 = b'$'
    FILE_6 = b'%'
    FILE_7 = b'&'
    FILE_8 = b"'"
    FILE_9 = b'('
    FILE_10 = b')'
    FILE_11 = b'*'
    FILE_12 = b'+'
    FILE_13 = b','
    FILE_14 = b'-'
    FILE_15 = b'.'
    FILE_16 = b'/'
    FILE_PRIORITY = b'0'
    FILE_17 = b'1'
    FILE_18 = b'2'
    FILE_19 = b'3'
    FILE_20 = b'4'
    FILE_21 = b'5'
    FILE_22 = b'6'
    FILE_23 = b'7'
    FILE_24 = b'8'
    FILE_25 = b'9'
    FILE_26 = b':'
    FILE_27 = b';'
    FILE_28 = b'<'
    FILE_29 = b'='
    FILE_30 = b'>'
    FILE_31 = b'?'
    FILE_32 = b'@'
    FILE_33 = b'A'
    FILE_34 = b'B'
    FILE_35 = b'C'
    FILE_36 = b'D'
    FILE_37 = b'E'
    FILE_38 = b'F'
    FILE_39 = b'G'
    FILE_40 = b'H'
    FILE_41 = b'I'
    FILE_42 = b'J'
    FILE_43 = b'K'
    FILE_44 = b'L'
    FILE_45 = b'M'
    FILE_46 = b'N'
    FILE_47 = b'O'
    FILE_48 = b'P'
    FILE_49 = b'Q'
    FILE_50 = b'R'
    FILE_51 = b'S'
    FILE_52 = b'T'
    FILE_53 = b'U'
    FILE_54 = b'V'
    FILE_55 = b'W'
    FILE_56 = b'X'
    FILE_57 = b'Y'
    FILE_58 = b'Z'
    FILE_59 = b'['
    FILE_60 = b'\\'
    FILE_61 = b']'
    FILE_62 = b'^'
    FILE_63 = b'_'
    FILE_64 = b'`'
    FILE_65 = b'a'
    FILE_66 = b'b'
    FILE_67 = b'c'
    FILE_68 = b'd'
    FILE_69 = b'e'
    FILE_70 = b'f'
    FILE_71 = b'g'
    FILE_72 = b'h'
    FILE_73 = b'i'
    FILE_74 = b'j'
    FILE_75 = b'k'
    FILE_76 = b'l'
    FILE_77 = b'm'
    FILE_78 = b'n'
    FILE_79 = b'o'
    FILE_80 = b'p'
    FILE_81 = b'q'
    FILE_82 = b'r'
    FILE_83 = b's'
    FILE_84 = b't'
    FILE_85 = b'u'
    FILE_86 = b'v'
    FILE_87 = b'w'
    FILE_88 = b'x'
    FILE_89 = b'y'
    FILE_90 = b'z'
    FILE_91 = b'{'
    FILE_92 = b'|'
    FILE_93 = b'}'
    FILE_94 = b'~'


# Note: 0x30 ("0") (int: 42) is reserved for priority (hence the name 'FILE_PRIORITY')

class TextPosition(_GetterEnum):
    """
    Text positions (useless for the BetaBrite, but position needs to be included in packets for validity)
    """
    MIDDLE: bytes = b" "  # center text vertically
    TOP: bytes = b"\""  # text begins at top and at most n-1 lines
    BOTTOM: bytes = b"&"  # text immediatly follows the TOP
    FILL: bytes = b"0"  # center text verically and use all


class TextMode(_GetterEnum):
    """
    Text modes / animations
    """
    ROTATE: bytes = b"a"  # rotate right to left
    HOLD: bytes = b"b"  # stationary
    FLASH: bytes = b"c"  # stationary and flash
    ROLLUP: bytes = b"e"  # push up old message by new message
    ROLLDOWN: bytes = b"f"  # push down old message by new message
    ROLLLEFT: bytes = b"g"  # push left old message by new message
    ROLLRIGHT: bytes = b"h"  # push right old message by new message
    WIPEUP: bytes = b"i"  # wipe up over old message with new
    WIPEDOWN: bytes = b"j"  # wipe down over old message with new
    WIPELEFT: bytes = b"k"  # wipe left over old message with new
    WIPERIGHT: bytes = b"l"  # wipe right over old message with new
    SCROLL: bytes = b"m"  # new message pushes the bottom line
    # to the top of a 2 line sign
    AUTO: bytes = b"o"  # random mode selected automatically
    ROLLIN: bytes = b"p"  # new message pushed inward
    ROLLOUT: bytes = b"q"  # new message pushed outward
    WIPEIN: bytes = b"r"  # new message wiped over old inward
    WIPEOUT: bytes = b"s"  # new message wiped over old outward
    CMPRSROT: bytes = b"t"  # rotate right to left with text
    # only half as wide
    TWINKLE: bytes = b"n0"  # twinkle message
    SPARKLE: bytes = b"n1"  # new message sparkles over the old
    SNOW: bytes = b"n2"  # snow the new message
    INTERLOCK: bytes = b"n3"  # new message interlocks over the old
    SWITCH: bytes = b"n4"  # switch "off" the old message char by
    # char.  new message switches "on"
    # char by char
    SLIDE: bytes = b"n5"  # slide chars right to left one at a
    # time
    SPRAY: bytes = b"n6"  # spray message right to left
    STARBURST: bytes = b"n7"  # explode new message
    WELCOME: bytes = b"n8"  # display a script "Welcome"
    SLOTMACHINE: bytes = b"n9"  # display slot machine reels
    NEWSFLASH: bytes = b"nA"  # display "Newsflash" animation
    TRUMPET: bytes = b"nB"  # display a trumpet animation
    THANKYOU: bytes = b"nS"  # display a script "Thank You"
    NOSMOKING: bytes = b"nU"  # display "No Smoking" animation
    DRINKDRIVE: bytes = b"nV"  # display "Don't Drink and Drive" animation
    ANIMAL: bytes = b"nW"  # display a running animal
    FISH: bytes = b"nW"  # display fish
    #   (BetaBrite alternate for ANIMAL)
    FIREWORKS: bytes = b"nX"  # display fireworks animation
    TURBOCAR: bytes = b"nY"  # display a car animation
    BALLOONS: bytes = b"nY"  # display a balloon animation
    #   (BetaBrite alternate for TURBOCAR)
    CHERRYBOMB: bytes = b"nZ"  # display a cherry bomb animation


class TextColor(_GetterEnum):
    """
    Text colors
    """
    RED: bytes = b"\x1c\x31"  # set text color to red
    GREEN: bytes = b"\x1c\x32"  # set text color to green
    AMBER: bytes = b"\x1c\x33"  # set text color to amber
    DIMRED: bytes = b"\x1c\x34"  # set text color to dim red
    DIMGREEN: bytes = b"\x1c\x35"  # set text color to dim green
    BROWN: bytes = b"\x1c\x36"  # set text color to brown
    ORANGE: bytes = b"\x1c\x37"  # set text color to orange
    YELLOW: bytes = b"\x1c\x38"  # set text color to yellow
    RAINBOW1: bytes = b"\x1c\x39"  # set text color to rainbow all chars
    RAINBOW2: bytes = b"\x1c\x41"  # set text color to rainbow indiv chars
    MIX: bytes = b"\x1c\x42"  # each char gets a differnt color
    AUTO: bytes = b"\x1c\x43"  # cycle through color modes


class TextCharacter(_GetterEnum):
    """
    Characters used in text
    """
    LF: bytes = b"\x0a"  # Line Feed
    CR: bytes = b"\x0d"  # Carriage Return (new line)
    CENTS: bytes = b"^"  # cents sign
    HALF_SPACE: bytes = b"~"  # half a space
    BLOCK_CHAR: bytes = b"\x7f"  # a square block character
    C_CEDILLA: bytes = b"\x80"  # capital 'c' with cedilla (i think)
    u_DIAERESIS: bytes = b"\x81"  # lowercase 'u' with diaeresis
    e_GRAVE: bytes = b"\x82"  # lowercase 'e' with grave
    a_CIRCUMFLEX: bytes = b"\x83"  # lowercase 'a' with circumflex
    a_DIAERESIS: bytes = b"\x84"  # lowercase 'a' with diaeresis
    a_ACUTE: bytes = b"\x85"  # lowercase 'a' with acute
    a_RING_ABOVE: bytes = b"\x86"  # lowercase 'a' with ring above
    c_CEDILLA: bytes = b"\x87"  # lowercase 'c' with cedilla
    e_CIRCUMFLEX: bytes = b"\x88"  # lowercase 'e' with circumflex
    e_DIAERESIS: bytes = b"\x89"  # lowercase 'e' with diaeresis
    i_DIAERESIS: bytes = b"\x8b"  # lowercase 'i' with diaeresis
    i_CIRCUMFLEX: bytes = b"\x8c"  # lowercase 'i' with circumflex
    i_GRAVE: bytes = b"\x8d"  # lowercase 'i' with grave
    A_DIAERESIS: bytes = b"\x8e"  # capital 'a' with diaeresis
    A_RING_ABOVE: bytes = b"\x8f"  # capital 'a' with ring above
    E_ACUTE: bytes = b"\x90"  # capital 'e' with acute
    ae_LIGATURE: bytes = b"\x91"  # lowercase 'ae' ligature
    AE_LIGATURE: bytes = b"\x92"  # capital 'ae' ligature
    o_CIRCUMFLEX: bytes = b"\x93"  # lowercase 'o' with circumflex
    o_DIAERESIS: bytes = b"\x94"  # lowercase 'o' with diaeresis
    o_GRAVE: bytes = b"\x95"  # lowercase 'o' with grave
    u_CIRCUMFLEX: bytes = b"\x96"  # lowercase 'u' with circumflex
    u_GRAVE: bytes = b"\x97"  # lowercase 'u' with grave
    y_DIAERESIS: bytes = b"\x98"  # lowercase 'y' with diaeresis
    O_DIAERESIS: bytes = b"\x99"  # capital 'o' with diaeresis
    U_DIAERESIS: bytes = b"\x9a"  # capital 'u' with diaeresis
    POUNDS: bytes = b"\x9c"  # british pounds sign
    YEN: bytes = b"\x9d"  # yen sign
    PERCENT: bytes = b"\x9e"  # percent sign
    FLORIN: bytes = b"\x9f"  # slant lowercase f
    i_ACUTE: bytes = b"\xa1"  # lowercase 'i' with acute
    o_ACUTE: bytes = b"\xa2"  # lowercase 'o' with acute
    u_ACUTE: bytes = b"\xa3"  # lowercase 'u' with acute
    n_TILDE: bytes = b"\xa4"  # lowercase 'n' with tilde
    N_TILDE: bytes = b"\xa5"  # capital 'n' with tilde
    SUPER_a: bytes = b"\xa6"  # superscript 'a'
    SUPER_o: bytes = b"\xa7"  # superscript 'o'
    INVERT_QUESTION: bytes = b"\xa8"  # inverted question mark
    DEGREES: bytes = b"\xa9"  # degree sign (superscript circle)
    INVERT_EXCLAIM: bytes = b"\xaa"  # inverted exclaimation mark
    SINGLE_COL_SPACE: bytes = b"\xab"  # single column space
    theta: bytes = b"\xac"  # lowercase theta
    THETA: bytes = b"\xad"  # capital theta
    c_ACUTE: bytes = b"\xae"  # lowercase 'c' with acute
    C_ACUTE: bytes = b"\xaf"  # capital 'c' with acute
    CHAR_c: bytes = b"\xb0"  # lowercase 'c'
    CHAR_C: bytes = b"\xb1"  # capital 'c'
    CHAR_d: bytes = b"\xb2"  # lowercase 'd'
    CHAR_D: bytes = b"\xb3"  # capital 'd'
    CHAR_s: bytes = b"\xb4"  # lowercase 's'
    CHAR_z: bytes = b"\xb5"  # lowercase 'z'
    CHAR_Z: bytes = b"\xb6"  # capital 'z'
    BETA: bytes = b"\xb7"  # beta
    CHAR_S: bytes = b"\xb8"  # capital 's'
    BETA2: bytes = b"\xb9"  # beta
    A_ACUTE: bytes = b"\xba"  # capital 'a' with acute
    A_GRAVE: bytes = b"\xbb"  # capital 'a' with grave accent
    A_2ACUTE: bytes = b"\xbc"  # capital 'a' with two accents
    a_2ACUTE: bytes = b"\xbd"  # lowercase ''a' with two accents
    I_ACUTE: bytes = b"\xbf"  # capital 'i' with accute
    O_TILDE: bytes = b"\xc0"  # capital 'o' with tilde
    o_TILDE: bytes = b"\xc1"  # lowercase 'o' with tilde
    XC_C_CEDILLA: bytes = b"\x08\x20"  # capital 'c' with cedilla
    XC_u_DIAERESIS: bytes = b"\x08\x21"  # lowercase 'u' with diaeresis
    XC_e_GRAVE: bytes = b"\x08\x22"  # lowercase 'e' with grave accent
    XC_a_CIRCUMFLEX: bytes = b"\x08\x23"  # lowercase 'a' with circumflex
    XC_a_DIAERESIS: bytes = b"\x08\x24"  # lowercase 'a' with diaeresis
    XC_a_ACUTE: bytes = b"\x08\x25"  # lowercase 'a' with accute
    XC_a_RING_ABOVE: bytes = b"\x08\x26"  # lowercase 'a' with ring above
    XC_c_CEDILLA: bytes = b"\x08\x27"  # lowercase 'c' with cedilla
    XC_e_CIRCUMFLEX: bytes = b"\x08\x28"  # lowercase 'e' with circumflex
    XC_e_DIAERESIS: bytes = b"\x08\x29"  # lowercase 'e' with diaeresis
    XC_i_DIAERESIS: bytes = b"\x08\x2b"  # lowercase 'i' with diaeresis
    XC_i_CIRCUMFLEX: bytes = b"\x08\x2c"  # lowercase 'i' with circumflex
    XC_i_GRAVE: bytes = b"\x08\x2d"  # lowercase 'i' with grave accent
    XC_A_DIAERESIS: bytes = b"\x08\x2e"  # capital 'a' with diaeresis
    XC_A_RING_ABOVE: bytes = b"\x08\x2f"  # capital 'a' with ring above
    XC_E_ACUTE: bytes = b"\x08\x30"  # capital 'e' with accute
    XC_ae_LIGATURE: bytes = b"\x08\x31"  # lowercase 'ae' ligature
    XC_AE_LIGATURE: bytes = b"\x08\x32"  # capital 'ae' ligature
    XC_o_CIRCUMFLEX: bytes = b"\x08\x33"  # lowercase 'o' with circumflex
    XC_o_DIAERESIS: bytes = b"\x08\x34"  # lowercase 'o' with diaeresis
    XC_o_GRAVE: bytes = b"\x08\x35"  # lowercase 'o' with grave accent
    XC_u_CIRCUMFLEX: bytes = b"\x08\x36"  # lowercase 'u' with circumflex
    XC_u_GRAVE: bytes = b"\x08\x37"  # lowercase 'u' with grave accent
    XC_y_DIAERESIS: bytes = b"\x08\x38"  # lowercase 'y' with diaeresis
    XC_O_DIAERESIS: bytes = b"\x08\x39"  # capital 'o' with diaeresis
    XC_U_DIAERESIS: bytes = b"\x08\x3a"  # capital 'u' with diaeresis
    XC_CENTS: bytes = b"\x08\x3b"  # cents sign
    XC_POUNDS: bytes = b"\x08\x3c"  # british pounds sign
    XC_YEN: bytes = b"\x08\x3d"  # yen sign
    XC_PERCENT: bytes = b"\x08\x3e"  # percent sign
    XC_SLANT_F: bytes = b"\x08\x3f"  # slant lowercase f
    XC_i_ACUTE: bytes = b"\x08\x41"  # lowercase 'i' with accute
    XC_o_ACUTE: bytes = b"\x08\x42"  # lowercase 'o' with accute
    XC_u_ACUTE: bytes = b"\x08\x43"  # lowercase 'u' with accute
    XC_n_TILDE: bytes = b"\x08\x44"  # lowercase 'n' with tilde
    XC_N_TILDE: bytes = b"\x08\x45"  # capital 'n' with tilde
    XC_SUPER_a: bytes = b"\x08\x46"  # superscript 'a'
    XC_SUPER_o: bytes = b"\x08\x47"  # superscript 'o'
    XC_INVERT_QUESTION: bytes = b"\x08\x48"  # inverted question mark
    XC_DEGREES: bytes = b"\x08\x49"  # degree sign (superscript circle)
    XC_INVERT_EXCLAIM: bytes = b"\x08\x4a"  # inverted exclaimation mark
    XC_SINGLE_COL_SPACE: bytes = b"\x08\x4b"  # single column space
    XC_theta: bytes = b"\x08\x4c"  # lowercase theta
    XC_THETA: bytes = b"\x08\x4d"  # capital theta
    XC_c_ACUTE: bytes = b"\x08\x4e"  # lowercase 'c' with accute
    XC_C_ACUTE: bytes = b"\x08\x4f"  # capital 'c' with accute
    XC_c: bytes = b"\x08\x50"  # lowercase 'c'
    XC_C: bytes = b"\x08\x51"  # capital 'c'
    XC_d: bytes = b"\x08\x52"  # lowercase 'd'
    XC_D: bytes = b"\x08\x53"  # capital 'd'
    XC_s: bytes = b"\x08\x54"  # lowercase 's'
    XC_z: bytes = b"\x08\x55"  # lowercase 'z'
    XC_Z: bytes = b"\x08\x56"  # capital 'z'
    XC_BETA: bytes = b"\x08\x57"  # beta
    XC_S: bytes = b"\x08\x58"  # capital 's'
    XC_BETA2: bytes = b"\x08\x59"  # beta
    XC_A_ACUTE: bytes = b"\x08\x5a"  # capital 'a' with accute
    XC_A_GRAVE: bytes = b"\x08\x5b"  # capital 'a' with grave accute
    XC_A_2ACUTE: bytes = b"\x08\x5c"  # capital 'a' with two accutes
    XC_a_2ACUTE: bytes = b"\x08\x5d"  # lowercase ''a' with two accutes
    XC_I_ACUTE: bytes = b"\x08\x5f"  # capital 'i' with accute
    XC_O_TILDE: bytes = b"\x08\x60"  # capital 'o' with tilde
    XC_o_TILDE: bytes = b"\x08\x61"  # lowecase 'o' with tilde


class SignAddress(_GetterEnum):
    """
    Sign addresses
    """
    SIGN_ADDRESS_BROADCAST: bytes = b"00"  # All signs on the network should "listen" to this transmission


class PacketCharacter(_GetterEnum):
    """
    Characters (and character sequences) only utilized in packets (i.e. not as text characters) that don't fit elsewhere
    """

    NUL: bytes = b"\x00"  # NULl
    WAKEUP: bytes = NUL * 5
    SOH: bytes = b"\x01"  # Start Of Header
    STX: bytes = b"\x02"  # Start Of TeXt
    SOM: bytes = b"\x1b"  # Start Of Mode
    ETX: bytes = b"\x03"  # End of TeXt
    EOT: bytes = b"\x04"  # End Of Transmission
    DBL_HEIGHT_CHARS_ON: bytes = b"\x05\x30"  # double height chars off (def)
    DBL_HEIGHT_CHARS_OFF: bytes = b"\x05\x31"  # double height chars on
    TRUE_DESCENDERS_ON: bytes = b"\x06\x30"  # true descenders off (default)
    TRUE_DESCENDERS_OFF: bytes = b"\x06\x31"  # true descenders on
    CHAR_FLASH_ON: bytes = b"\x07\x30"  # character flash off (default)
    CHAR_FLASH_OFF: bytes = b"\x07\x31"  # character flash off (default)
    TEMP_CELSIUS: bytes = b"\x08\x1c"  # current temperature in celsius
    TEMP_FAHRENHEIT: bytes = b"\x08\x1d"  # current temperature in fahrenheit

    COUNTER_1: bytes = b"\x08\x7a"  # current value in counter 1
    COUNTER_2: bytes = b"\x08\x7b"  # current value in counter 2
    COUNTER_3: bytes = b"\x08\x7c"  # current value in counter 3
    COUNTER_4: bytes = b"\x08\x7d"  # current value in counter 4
    COUNTER_5: bytes = b"\x08\x7e"  # current value in counter 4
    NO_HOLD_SPEED: bytes = b"\x09"  # no hold speed (no pause following the mode presentation. Not applicable to ROTATE or
    #   COMPRESSED_ROTATE modes)
    CURDATE_MMDDYY_SLASH: bytes = b"\x0b\x30"  # current date MM/DD/YY
    CURDATE_DDMMYY_SLASH: bytes = b"\x0b\x31"  # current date DD/MM/YY
    CURDATE_MMDDYY_DASH: bytes = b"\x0b\x32"  # current date MM-DD-YY
    CURDATE_DDMMYY_DASH: bytes = b"\x0b\x33"  # current date DD-MM-YY
    CURDATE_MMDDYY_DOT: bytes = b"\x0b\x34"  # current date MM.DD.YY
    CURDATE_DDMMYY_DOT: bytes = b"\x0b\x35"  # current date DD.MM.YY
    CURDATE_MMDDYY_SPACE: bytes = b"\x0b\x36"  # current date MM DD YY
    CURDATE_DDMMYY_SPACE: bytes = b"\x0b\x37"  # current date DD MM YY
    CURDATE_MMMDDYYYY: bytes = b"\x0b\x38"  # current date MMM.DD, YYYY
    CURDATE_WEEKDAYY: bytes = b"\x0b\x39"  # current day of week
    NEW_PAGE: bytes = b"\x0c"  # start next display page
    STRING_FILE_INSERT: bytes = b"\x10"  # insert STRING file (next char is
    #   the filename)
    WIDE_CHARS_OFF: bytes = b"\x11"  # disable wide characters
    WIDE_CHARS_ON: bytes = b"\x12"  # enables wide characters
    CALL_TIME: bytes = b"\x13"
    DOTS_INSERT: bytes = b"\x14"  # insert DOTS picture (next char is
    #   the filename)
    SPEED_1: bytes = b"\x15"  # set scroll speed to 1 (slowest)
    SPEED_2: bytes = b"\x16"  # set scroll speed to 2
    SPEED_3: bytes = b"\x17"  # set scroll speed to 3
    SPEED_4: bytes = b"\x18"  # set scroll speed to 4
    SPEED_5: bytes = b"\x19"  # set scroll speed to 5 (fastest)
    CHARSET_5_NORMAL: bytes = b"\x1a\x31"  # set character set 5 high normal
    CHARSET_7_NORMAL: bytes = b"\x1a\x33"  # set character set 7 high normal
    CHARSET_7_FANCY: bytes = b"\x1a\x35"  # set character set 7 high fancy
    CHARSET_10_NORMAL: bytes = b"\x1a\x36"  # set character set 10 high normal
    CHARSET_FULL_FANCY: bytes = b"\x1a\x38"  # set character set full height fancy
    CHARSET_FULL_NORMAL: bytes = b"\x1a\x39"  # set character set full height normal

    CHAR_ATTRIB_WIDE_ON: bytes = b"\x1d\x30\x31"  # char attrib wide on
    CHAR_ATTRIB_WIDE_OFF: bytes = b"\x1d\x30\x30"  # char attrib wide off
    CHAR_ATTRIB_DBLW_ON: bytes = b"\x1d\x31\x31"  # char attrib dbl width on
    CHAR_ATTRIB_DBLW_OFF: bytes = b"\x1d\x31\x30"  # char attrib dbl width off
    CHAR_ATTRIB_DBLH_ON: bytes = b"\x1d\x32\x31"  # char attrib dbl height on
    CHAR_ATTRIB_DBLH_OFF: bytes = b"\x1d\x32\x30"  # char attrib dbl height off
    CHAR_ATTRIB_DESC_ON: bytes = b"\x1d\x33\31"  # char attrib true desc on
    CHAR_ATTRIB_DESC_OFF: bytes = b"\x1d\x33\30"  # char attrib true desc off
    CHAR_ATTRIB_FIX_ON: bytes = b"\x1d\x34\x31"  # char attrib fixed width on
    CHAR_ATTRIB_FIX_OFF: bytes = b"\x1d\x34\x30"  # char attrib fixed width off
    CHAR_ATTRIB_FNCY_ON: bytes = b"\x1d\x35\x31"  # char attrib fancy on
    CHAR_ATTRIB_FNCY_OFF: bytes = b"\x1d\x35\x30"  # char attrib fancy off
    FIXED_WIDTH_OFF: bytes = b"\x1e\x30"  # fixed width chars off (default)
    FIXED_WIDTH_ON: bytes = b"\x1e\x31"  # fixed width chars on
    ALPHA_DOTS_INSERT: bytes = b"\x1f"  # insert ALPHAVISION DOTS picture
#   must be followed by:
#   SFFFFFFFFFtttt
#     S = b"C" file is part of a
#               QuickFlick animation.
#               Clear display and uses
#               hold time
#     S = b"L" file is a DOTS picture.
#               if inserted in a
#               TEXT file, then hold
#               time is ignored
#     Fx9 = filename (pad with SPACEs)
#     tttt = 4 digit ascii hexnum
#              indicating tenths of
#              of seconds
