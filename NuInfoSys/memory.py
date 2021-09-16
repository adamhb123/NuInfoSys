from typing import Dict, Union
from enum import Enum
import betabrite
from framecontrolbytes import *

# Temporary memory dict
MEMORY_LAYOUT: Dict[bytes, int] = {
    FileName.FILE_PRIORITY: 25000,
}



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
