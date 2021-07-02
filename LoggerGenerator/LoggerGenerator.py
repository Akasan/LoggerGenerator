import sys
from datetime import datetime
import logging
from abc import abstractmethod, ABCMeta
import os
from .Exceptions import *

_LEVEL2TXT = {
    0: "NOT SET",
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL",
}

_TXT2LEVEL = {v: k for k, v in _LEVEL2TXT.items()}


class LoggerGenerator:
    """
    Examples:
    ---------
        >>> from LoggerGenerator import logger_gen
        >>> logger_gen(globals())
        >>> log.info("...")
    """
    def __init__(self):
        self._is_generated = False
        self._LOG_FOLDER = "./"
        self._LOG_FOLDER_SET = False
        self._log = None
        self._pre_level = None
        self._FILENAME = None
        self._FORMAT = "%(asctime)s - %(levelname)s (%(filename)s) : %(message)s"
        self._IS_PRINT = True
        self._IS_FILE = True

    def check_initialize(base: bool = True):
        """ check _is_generated"""
        def _check_initialize(func):
            def _wrapper(self, *args, **kwargs):
                assert self._is_generated == base
                return func(self, *args, **kwargs)

            return _wrapper

        return _check_initialize

    @check_initialize()
    def get_level(self) -> str:
        """Get log level

        Returns:
        --------
            {str} -- log level 

        Examples:
        ---------
            >>> from LoggerGenerator import logger_gen
            >>> logger_gen.get_level()      # Raise exception because logger is not generated.
            >>> logger_gen(globals())       # Once call this code, logger is generated.
            >>> logger_gen.get_level()
        """
        global _LEVEL2TXT
        return _LEVEL2TXT[self._log.level]

    @check_initialize()
    def set_level(self, level: str) -> str:
        global _TXT2LEVEL
        assert level in _TXT2LEVEL
        self._pre_level = self._log.level
        self._log.setLevel(_TXT2LEVEL[level])

    @check_initialize()
    def stop(self):
        self._pre_level = self._log.level
        self._log.setLevel(1000)

    @check_initialize()
    def restart(self):
        self._log.setLevel(self._pre_level)

    @check_initialize(False)
    def set_filename(self, filename: str):
        self._FILENAME = filename

    @check_initialize(False)
    def set_format(self, _format: str):
        self._FORMAT = _format

    @check_initialize(False)
    def set_folder(self, log_folder: str):
        assert os.path.exists(log_folder)
        assert not self._LOG_FOLDER_SET, AlreadySetFolderException()

        self._LOG_FOLDER = log_folder
        if not self._LOG_FOLDER[-1] == "/":
            self._LOG_FOLDER += "/"

        self._LOG_FOLDER_SET = True

    @check_initialize(False)
    def set_print_stauts(self, status: bool):
        self._IS_PRINT = status

    @check_initialize(False)
    def set_file_status(self, status: bool):
        self._IS_FILE = status


    @check_initialize(False)
    def _generate_log(self):
        self._is_generated = True
        now = datetime.now()
        year = str(now.year)
        month = str(now.month).zfill(2)
        day = str(now.day).zfill(2)
        hour = str(now.hour).zfill(2)
        minute = str(now.minute).zfill(2)
        second = str(now.second).zfill(2)

        if self._FILENAME is None:
            filename = f"{self._LOG_FOLDER}{year}{month}{day}-{hour}{minute}{second}.log"
        else:
            filename = self._FILENAME

        self._log = logging.getLogger(__name__)
        self._log.setLevel(logging.DEBUG)
        fmt = logging.Formatter(self._FORMAT)

        if self._IS_PRINT:
            sh = logging.StreamHandler(sys.stdout)
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(fmt)
            self._log.addHandler(sh) 
        
        if self._IS_FILE:
            fh = logging.FileHandler(filename)
            fh.setFormatter(fmt)
            self._log.addHandler(fh)

    def __call__(self, g: dict) -> logging.RootLogger:
        if not self._is_generated:
            self._generate_log()

        g["log"] = self._log


logger_gen = LoggerGenerator()
