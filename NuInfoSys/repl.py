import re
from serial import Serial
from typing import List, Union, Optional, Dict

from NuInfoSys import config
from NuInfoSys.framecontrolbytes import *

HELP_MESSAGE: str = '''WARNING: <NUL>*5 + <SOH> + !00 (type code + sign address) + <STX> is prepended, and <EOT> is appended to all console commands for convenience
NuInfoSys REPL Usage:
    [EXAMPLES]
    $ CLEARMEM = E$ -> clears memory
    
    [CONFIGURATION]
    RECEIVE={True, False} - Sets whether or not the REPL should wait for a
    response from the sign after sending a command. If set to True, the
    program will wait until it receives data back from the sign OR after the
    5 second timeout duration expires.
    
    E$#ALFFFF4000 -> This (should) appropriately set memory!!
    '''
# PacketCharacter.NUL * 5 + PacketCharacter.SOH + SignType.SIGN_TYPE_ALL_VERIFY +
#                     SignAddress.SIGN_ADDRESS_BROADCAST + PacketCharacter.STX + command_bytes +
#                  PacketCharacter.EOT
STRING_TO_NONPRINTABLE: Dict[str, bytes] = {
    "STX": PacketCharacter.STX,
    "EOT": PacketCharacter.EOT,
    "SOH": PacketCharacter.SOH,
    "SOM": PacketCharacter.SOM,
    "NUL": PacketCharacter.NUL,
    "ETX": PacketCharacter.ETX
}

COMMAND_ALIASES: Dict[str, bytes] = {
    "CLEARMEM": PacketCharacter.SOH + SignType.SIGN_TYPE_ALL_VERIFY + SignAddress.SIGN_ADDRESS_BROADCAST + PacketCharacter.STX + b'E$' + PacketCharacter.EOT
}


def main() -> None:
    """
    REPL
    """
    ser: Optional[Serial] = None
    if config.CLI_ALLOW_TRANSMISSION:
        ser: Serial = Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=5)

    receive_mode: bool = False
    print(HELP_MESSAGE)
    while True:
        command: str = input(f"[RECEIVE: {receive_mode}]$ ")
        command_bytes: bytes = b""
        # Parse setting change, could use a dict for this if more settings come up
        if "RECEIVE=" in command:
            choice: str = command.split('=')[1].lower()
            receive_mode: bool = True if choice == "true" else False
        # Parse PacketCharacters such as <NUL>, <SOH>, etc
        command_split: List[Union[str, bytes]] = list(filter(None, re.split("(<.*?>)|(\\\\x.{2})", command)))
        if len(command_split):
            for i in range(0, len(command_split)):
                if command_split[i] in COMMAND_ALIASES:
                    command_split: List[Union[str,bytes]] = [COMMAND_ALIASES[command_split[i]]]
                    break
                if command_split[i]:
                    if command_split[i][0] == "<":
                        command_split[i]: bytes = STRING_TO_NONPRINTABLE[command_split[i][1:len(command_split[i]) - 1]]
                    elif command_split[i][0:2] == "\\x":
                        command_split[i]: bytes = eval(command_split[i])

        for item in command_split:
            print(item)
            if item:
                command_bytes += bytes(item, "utf-8") if isinstance(item, str) else item
        print(command_bytes)

        print(":".join("{:02x}".format(ord(c)) for c in str(command_bytes)))
        print(command_bytes)
        if ser is not None:
            packet: bytes = PacketCharacter.NUL * 5 + PacketCharacter.SOH + SignType.SIGN_TYPE_ALL_VERIFY + \
                            SignAddress.SIGN_ADDRESS_BROADCAST + PacketCharacter.STX + command_bytes + PacketCharacter.EOT
            ser.write(packet)
            # Wait for response if in receive mode
            if receive_mode:
                received: bytes = ser.read_until(PacketCharacter.EOT)
                print(f"RECEIVED FROM SIGN: {received}")


if __name__ == "__main__":
    main()
