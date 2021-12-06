import re
from serial import Serial
from typing import List

from NuInfoSys import config
from NuInfoSys.framecontrolbytes import *

HELP_MESSAGE: str = '''NuInfoSys REPL Usage:
    [EXAMPLES]
    $ E$ - clears memory
    $ E$ - clears memory
    [CONFIGURATION]
    RECEIVE={True, False} - Sets whether or not the REPL should wait for a
    response from the sign after sending a command. If set to True, the
    program will wait until it receives data back from the sign OR after the
    5 second timeout duration expires.'''

STRING_TO_NONPRINTABLE = {
    "STX": PacketCharacter.STX,
    "EOT": PacketCharacter.EOT,
    "SOH": PacketCharacter.SOH,
    "SOM": PacketCharacter.SOM,
    "NUL": PacketCharacter.NUL,
    "ETX": PacketCharacter.ETX
}


def main():
    """
    REPL
    """
    ser: Serial = Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=5)
    receive_mode: bool = False
    print(HELP_MESSAGE)
    while True:
        command: str = input(f"[RECEIVE: {receive_mode}]$ ")
        # Parse setting change, could use a dict for this if more settings come up
        if "RECEIVE=" in command:
            choice: str = command.split('=')[1].lower()
            receive_mode: bool = True if choice == "true" else False
        command_split: List[str] = re.split("(<.*?>)", command)
        for i in range(0, len(command_split)):
            if command_split[i][0] == "<":
                command_split[i] = STRING_TO_NONPRINTABLE[command_split[i][1:len(command_split)-1]]
        command: str = ''.join(command_split)

        # Send command
        ser.write(PacketCharacter.NUL * 5 + PacketCharacter.SOH + SignType.SIGN_TYPE_ALL_VERIFY +
                  SignAddress.SIGN_ADDRESS_BROADCAST + PacketCharacter.STX + bytes(command, "utf-8") +
                  PacketCharacter.EOT)
        # Wait for response if in receive mode
        if receive_mode:
            received: bytes = ser.read_until(PacketCharacter.EOT)
            print(f"RECEIVED FROM SIGN: {received}")


if __name__ == "__main__":
    main()
