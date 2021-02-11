import inspect
import logging
import sys
import traceback

import colorlog
from colorlog import escape_codes
from tqdm import tqdm
from easylogger import get_logging_options_from_env

log_colors = {
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'black,bg_green',
}


class Logger(logging.Logger):

    def __init__(self, name, log_file=None, log_level_file=logging.DEBUG, log_level_console=logging.INFO,
                 color_file=True, color_console=True, time_in_formatter=False):
        self.log_level_console = log_level_console
        self.log_level_file = log_level_file
        self.log_file = log_file
        self.color_file = color_file
        self.color_console = color_console
        self.time_in_formatter = time_in_formatter
        self.name = name
        super(Logger, self).__init__(name)
        using_log_file = log_file is not None
        self.setLevel(log_level_file if using_log_file else log_level_console)
        if using_log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(log_level_file)
            fh.setFormatter(self.formatter(time_in_formatter, color_file))
            self.addHandler(fh)
        ch = colorlog.StreamHandler()
        ch.setLevel(log_level_console)
        ch.setFormatter(self.formatter(time_in_formatter, color_console))
        self.addHandler(ch)
        return

    def copy(self, new_name=None):
        if new_name is None:
            new_name = self.name
        return Logger(new_name, **self.logging_options)

    @property
    def logging_options(self):
        return dict(log_file=self.log_file, log_level_file=self.log_level_file,
                    log_level_console=self.log_level_console)

    def formatter(self, time=False, color=True):
        res = '%(levelname)s:%(name)s:   %(message)s'
        if time:
            res = "%(asctime)s  " + res
        if color:
            res = "%(log_color)s" + res
        if color:
            formatter = colorlog.ColoredFormatter(res, log_colors=log_colors)
        else:
            formatter = logging.Formatter(res)
        return formatter


class LoggingClass(object):
    def __init__(self, name=None, log=None, **kwargs):
        self.__name = name = name if name is not None else self.__class__.__name__
        kwargs = {**get_logging_options_from_env(), **kwargs}
        if log is not None:
            self.__log = log.copy(name)
        else:
            self.__log = Logger(name, **kwargs)

    @property
    def log(self):
        return self.__log

    def reset_log(self):
        self.__log = Logger(self.__name, **self.logging_options)

    def warning(self, *args, **kwargs):
        self.__log.warning(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.__log.debug(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.__log.error(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.__log.info(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.__log.critical(*args, **kwargs)

    @staticmethod
    def tqdm(it=None, log_level=logging.DEBUG, **kwargs):
        # noinspection PyProtectedMember
        level_name = logging._levelToName[log_level]
        colors = (escape_codes[log_colors[level_name]], escape_codes["reset"])
        if "bar_format" not in kwargs:
            kwargs["bar_format"] = "{l_bar}{bar}{r_bar}"
        kwargs["bar_format"] = kwargs["bar_format"].replace("{bar}", "%s{bar}%s" % colors)
        return tqdm(it, file=sys.stdout, **kwargs)

    @property
    def logging_options_names(self):
        return list(inspect.signature(Logger.__init__).parameters)[2:]

    @property
    def logging_options(self):
        elements = self.logging_options_names
        result = {i: getattr(self.__log, i) for i in elements}
        return result

    def assert_error(self, condition: bool, message: str):
        if not condition:
            self.error(message)

    def get_traceback(self) -> str:
        return traceback.format_exc()

    def filter_kwargs(self, **kwargs):
        names = self.logging_options_names
        kwargs1 = {k: v for k, v in kwargs.items() if k in names}
        kwargs2 = {k: v for k, v in kwargs.items() if k not in names}
        return kwargs1, kwargs2
