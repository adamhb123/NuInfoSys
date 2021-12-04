import time
from NuInfoSys import betabrite
from NuInfoSys.framecontrolbytes import *
from NuInfoSys.memory import Memory, File, TextFile, StringFile, DOTSFile

FILE_DISPLAY_WIDTH: int = 20


class MemoryVisual:
    def __init__(self,
                 memory: Memory):
        self.memory: Memory = memory
        self.file_visuals = [FileVisual(file) for file in self.memory.files]

    def __str__(self) -> str:
        memory_rep_str = ""
        for filevis in self.file_visuals:
            memory_rep_str += str(filevis)
        return memory_rep_str


class FileVisual:
    def __init__(self, file: File):
        self.file: File = file

    def __str__(self) -> str:
        """
        Returns string representation of file
        """
        file_rep_str: str = f" {'_' * FILE_DISPLAY_WIDTH}\n"
        file_rep_str += f"| File Name: {self.file.name[:FILE_DISPLAY_WIDTH - 4]}\n"
        file_rep_str += f"| File Type: {self.file.__class__.__name__}\n"
        file_rep_str += f"| {f'Allocated Memory: {self.file.memory}' if isinstance(self.file, StringFile) or isinstance(self.file, TextFile) else f'Image Dimensions: {self.file.width}x{self.file.height}'}\n"
        file_rep_str += f"|{'_' * FILE_DISPLAY_WIDTH}\n"
        return file_rep_str


def mts(message: str, seconds: int = 5, console_out: bool = True, file: FileName = FileName.FILE_PRIORITY,
        addr: bytes = SignAddress.SIGN_ADDRESS_BROADCAST,
        ttype: bytes = SignType.SIGN_TYPE_BETABRITE):
    """
    Sends message to display and then sleeps for seconds
    :param message: Message to display
    :param seconds: Seconds to sleep
    :param console_out: Whether or not to print to console
    :param addr: Sign address
    :param ttype: Sign type
    :param file: File to write to
    """
    """
    Message, then sleep
    :param seconds: seconds to sleep after sending the message
    :return: None
    """
    betabrite.send_animations(betabrite.Animation(message, mode=betabrite.TextMode.CMPRSROT), file=file, addr=addr,
                              ttype=ttype)
    if console_out:
        print(f"[MTS] {message}")
    time.sleep(seconds)


if __name__ == "__main__":
    memory = Memory([TextFile(b"Test1", True, memory=10), TextFile(b"Test2", True, memory=20)])
    mv = MemoryVisual(memory)
    print(str(mv))
