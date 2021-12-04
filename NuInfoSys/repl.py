from serial import Serial
from NuInfoSys import config
from NuInfoSys.framecontrolbytes import *

HELP_MESSAGE: str = '''NuInfoSys REPL Usage:
    [CONFIGURATION]
    RECEIVE={True, False} - Sets whether or not the REPL should wait for a
    response from the sign after sending a command. If set to True, the
    program will wait until it receives data back from the sign OR after the
    5 second timeout duration expires.'''


def main():
    ser: Serial = Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=5)
    receive_mode: bool = False
    print(HELP_MESSAGE)
    while True:
        command: str = input(f"[RECEIVE MODE: {receive_mode}]")
        if "RECEIVE=" in command:
            choice: str = command.split('=')[1].lower()
            receive_mode: bool = True if choice == "true" else False
        if receive_mode:
            received: bytes = ser.read_until(PacketCharacter.EOT)
            print(f"RECEIVED FROM SIGN: {received}")
        ser.write(command)


if __name__ == "__main__":
    main()
