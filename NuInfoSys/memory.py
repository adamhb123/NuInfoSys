from typing import Dict, Union, Optional, Callable, List
from enum import Enum
from NuInfoSys import betabrite
from NuInfoSys.framecontrolbytes import *

"""
Please note that all classes inheriting File (as well as File itself) are abstractions of the memorial properties of
the actual files that will be stored in the display. This means that these classes do not contain the actual information
that will be displayed on the screen (though we do need to know the width and height parameters here for DOTS files).
That is instead handled in betabrite.py.
"""


def _validate_parameter(parameter: Any, expected_types: Union[type, List[type]],
                        callback: Optional[Callable] = None) -> Any:
    """
    Validates the given parameter and calls a callback function if provided

    :param blahblah:
    :return: Result of callback's invocation, or parameter if no callback is given
    """
    found: bool = False
    if callback is not None and not isinstance(callback, Callable):
        raise ValueError(f"Invalid argument: '{callback}', expected: type={Callable}")
    if isinstance(expected_types, type):
        expected_types = [expected_types]

    for t in expected_types:
        if isinstance(parameter, t):
            found = True
    if not found:
        raise ValueError(f"Invalid argument: '{parameter}', expected: type={expected_types}")
    if callback is not None:
        return callback()
    return parameter


class File:
    """
    Abstract, high level representation of a file in memory
    """

    def __init__(self, name: bytes, locked: Union[bool, bytes] = True):
        """
        Class initializer

        :param name: The file's name (synonymous with label)
        :param file_type: The file's type
        :param locked: The file's lock state
        """

        self.name = _validate_parameter(name, bytes)
        self.locked = _validate_parameter(locked, [bool, bytes], lambda: locked if isinstance(locked, bytes) else (
            FileLock.LOCKED if locked else FileLock.UNLOCKED))

    def bytes(self) -> bytes:
        """
        Returns the Special Functions Data of this particular file (see protocol reference), to be overridden
        """
        pass


class TextFile(File):

    def __init__(self, name: bytes, locked: bool = True, memory: Union[bytes, int] = 0,
                 start_time: bytes = TextFileTime.ALWAYS, stop_time: bytes = TextFileTime.ALWAYS) -> None:
        self.memory: bytes = _validate_parameter(memory, [bytes, int], lambda: memory.to_bytes(2, "big") if isinstance(
            memory, int) else memory)
        self.start_time: bytes = _validate_parameter(start_time, bytes)
        self.stop_time: bytes = _validate_parameter(start_time, bytes)
        super().__init__(name, locked)

    def bytes(self) -> bytes:
        return self.name + FileType.TEXT + self.locked + self.memory + self.start_time + self.stop_time


class DOTSFile(File):
    def __init__(self, name: bytes, width: Union[bytes, int], height: Union[bytes, int], locked: bool = True,
                 color_status: bytes = DOTSColorStatus.EIGHT_COLOR) -> None:
        if name == FileName.FILE_PRIORITY:
            raise ValueError(
                "Invalid argument: 'name'=FileName.FILE_PRIORITY, "
                "FILE_PRIORITY cannot be made a DOTS file or STRING file, it is strictly a TEXT file")

        super().__init__(name, locked)

        self.width: bytes = _validate_parameter(width, [bytes, int],
                                                lambda: width if isinstance(width, bytes) else width.to_bytes(1, "big"))
        self.height: bytes = _validate_parameter(height, [bytes, int],
                                                 lambda: height if isinstance(
                                                     height, bytes) else height.to_bytes(1, "big"))
        self.color_status = _validate_parameter(color_status, bytes)

    def bytes(self) -> bytes:
        return self.name + FileType.DOTS + self.locked + self.height + self.width + self.color_status


class StringFile(File):

    def __init__(self, name: bytes, memory: Union[bytes, int]) -> None:
        if name == FileName.FILE_PRIORITY:
            raise ValueError(
                "Invalid argument: 'name'=FileName.FILE_PRIORITY, "
                "FILE_PRIORITY cannot be made a DOTS file or STRING file, it is strictly a TEXT file")
        # Note: all string files have to be locked, so we force True here
        super().__init__(name, True)
        self.memory: bytes = _validate_parameter(memory, [bytes, int],
                                                 lambda: memory.to_bytes(2, "big") if isinstance(
                                                     memory, int) else memory)

    def bytes(self) -> bytes:
        """
        Bytes representation
        b"0000" is appended as a placeholder for the STRING file. If it is not added then transmission fails.
        """
        return self.name + FileType.STRING + self.locked + self.memory + b"0000"


# DOTS  self.width = width if isinstance(width, int) else int.from_bytes(width, 'big')
# self.height = height if isinstance(height, int) else int.from_bytes(height, 'big')

class Memory:
    """
    High level representation of the sign's memory
    """

    def __init__(self, files: Optional[List[File]] = None) -> None:
        # Validate files parameter
        # Can't use generic checks due to optional, must check manually
        if files is not None:
            for file in files:
                _validate_parameter(file, File)

        self.files: List[File] = files if files is not None else []

    def get_file_by_name(self, name: bytes) -> File:
        """
        Gets the first file associated with the given name parameter

        :param name: Name of file to retrieve
        """
        return next(file for file in self.files if file.name == name)

    def get_all_files_of_type(self, file_type: bytes) -> List[File]:
        """
        :param file_type: Type of file to retrieve
        """
        return list(filter(lambda file: file.type == file_type, self.files))

    def clear(self, files_only: bool = False) -> Union[bytes, None]:
        """
        Clears all memory of files. Also clears the sign, unless files_only is set to True

        :return: Returns the bytes necessary to clear the sign memory, or None if files_only is set to True
        """
        for file in self.files:
            file.memory = 0

        if not files_only:
            return CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.MODIFY_MEMORY

    def flash(self) -> bytes:
        """
        [UNTESTED]
        Returns the bytes necessary to flash the memory map to the betabrite.

        :return: Bytes to be sent in packet
        """
        if len(self.files) == 0:
            raise ValueError("Cannot flash an empty memory mapping")
        return CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.MODIFY_MEMORY + b''.join(
            [file.bytes() for file in self.files])


'''
class MemoryConfigurationType(Enum):
    """
    Memory configuration options
    ALL_FILES_EQUAL: indicates that each of the 65 available files should share an equal amount of memory
    FIRST_FILE_MAX: lazy method, indicates that the first (non-priority) file should have all the memory
    CUSTOM: indicates that memory allocation will be defined by some dictionary
    """
    ALL_FILES_EQUAL = 0
    FIRST_FILE_MAX = 1
    CUSTOM = 2



I want to redo all this




class Memory:
    """
    Handles memory allocation

    Here is what a custom memory map would look look like

    MemoryMap: Dict[bytes, int] = {
        FILE_NORMAL_RANGE[0]: 1000, # == 1000 bytes of data allocated to the first non-priority file
        FILE_NORMAL_RANGE[1]: 2000, # == 2000 bytes of data allocated to the first non-priority file
        .
        .
        .
    }
    """

    def __init__(self, memory_configuration: Union[
            MemoryConfigurationType, Dict[FileName, int]] = MemoryConfigurationType.FIRST_FILE_MAX):
        self.map: Dict[FileName, int] = self._memory_map_from_configuration(memory_configuration)
        print(f"MAP CONFIGURATION: {self.map}")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.map.__str__()

    @staticmethod
    def _memory_map_from_configuration(config: MemoryConfigurationType) -> Dict[FileName, int]:
        """
        Writing this will be / is a pain in my ass
        FileName is a normal Enum, unlike most, which are _GetterEnum
        """
        if config == MemoryConfigurationType.FIRST_FILE_MAX:
            return {k: TOTAL_MEMORY if k == FileName.FILE_1 else 0 for k in FileName}  # type: ignore
        elif config == MemoryConfigurationType.ALL_FILES_EQUAL:
            return {k: TOTAL_MEMORY / len(FileName) for k in FileName}  # type: ignore
        else:
            raise Exception({
                ValueError("Inappropriate argument: 'config'"),
                MemoryConfigurationError("Inappropriate MemoryConfigurationType specified")
            })

    #def bytes(self) -> bytes:
        #return b''.join([k.value for k in self.map.keys()])

    @staticmethod
    def clear():
        """
        [TESTED, WORKING]
        Clears the sign memory
        """
        betabrite._transmit(CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.MODIFY_MEMORY)

    def flash(self):
        """
        [UNTESTED]
        Flashes the memory map to the betabrite
        """
        # to be rewritten
        betabrite._transmit(CommandCode.COMMAND_WRITE_SPECIAL + WriteSpecialFunctionsLabel.MODIFY_MEMORY + b''.join(
            [b"%s%s%s%s%s" % (
                k.value, FileType.TEXT, FileLock.LOCKED, v.to_bytes(4, 'big'),
                TextFileStartTime.TEXT_FILE_START_TIME_ALWAYS) for
             k, v in self.map.items()]))


class MemoryConfigurationError(Exception):
    def __init__(self, message):
        super().__init__(message)
'''

if __name__ == "__main__":
    mem = Memory()
    mem.files.append(TextFile(FileName.FILE_4, True, 1000))
    mem.files.append(DOTSFile(FileName.FILE_3, 7, 5))
    mem.files.append(StringFile(FileName.FILE_2, 0))
    print(mem.files[0].bytes())
    print(mem.files[1].bytes())
    print(mem.files[2].bytes())
    print(mem.flash())
