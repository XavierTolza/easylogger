from os import getenv
import logging


def get_logging_options_from_env():
    res = dict(
        log_file=("LOG_FILE", None),
        log_level_file=('LOG_LEVEL_FILE', "DEBUG"),
        log_level_console=('LOG_LEVEL_CONSOLE', "INFO"),
        color_file=("LOG_COLOR_FILE", False),
        color_console=("LOG_COLOR_CONSOLE", True),
        time_in_formatter=("LOG_TIME_IN_FORMATTER", True)
    )
    res = {k: getenv(v, default) for k, (v, default) in res.items()}

    # Change levels type
    for k, v in res.items():
        if "log_level" in k.lower():
            res[k] = getattr(logging, v)
        elif (v_str := str(v).lower()) in ("true", "false"):
            res[k] = True if v_str[0] == "t" else False

    return res
