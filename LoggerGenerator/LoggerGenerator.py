import sys
from datetime import datetime
import logging
from abc import abstractmethod, ABCMeta
import os


class LoggerGeneratorBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self) -> logging.RootLogger:
        pass


class LoggerGenerator(LoggerGeneratorBase):
    """
    Examples:
    ---------
        >>> from LoggerGenerator import logger_gen
        >>> logger_gen(globals())
        >>> log.info("...")
    """

    def __init__(self):
        self._is_generated = False
        self.__LOG_FOLDER = "./"

    def set_folder(self, log_folder: str):
        assert os.path.exists(log_folder)
        self.__LOG_FOLDER = log_folder
        if not self.__LOG_FOLDER[-1] == "/":
            self.__LOG_FOLDER += "/"

    def _generate_log(self):
        self._is_gegerated = True
        now = datetime.now()
        year = str(now.year)
        month = str(now.month).zfill(2)
        day = str(now.day).zfill(2)
        hour = str(now.hour).zfill(2)
        minute = str(now.minute).zfill(2)
        second = str(now.second).zfill(2)
        filename = f"{self.__LOG_FOLDER}{year}{month}{day}-{hour}{minute}{second}.log"
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        fh = logging.FileHandler(filename)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s (%(filename)s) : %(message)s")
        fh.setFormatter(fmt)
        sh.setFormatter(fmt)
        self.log.addHandler(fh)
        self.log.addHandler(sh) 

    def __call__(self, g: dict) -> logging.RootLogger:
        if not self._is_generated:
            self._generate_log()

        g["log"] = self.log


logger_gen = LoggerGenerator()
