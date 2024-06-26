## Shamelessly stolen from my sensor-stasher repo - See: https://github.com/naschorr/sensor-stasher/blob/main/code/utilities.py

import json
import logging
import datetime
import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

from jsonc_parser.parser import JsoncParser

## Config
CONFIG_NAME = "config"	                # The name of the config file
DEV_CONFIG_NAME = "config.dev"          # The name of the dev config file (overrides properties stored in the normal and prod config files)
PROD_CONFIG_NAME = "config.prod"        # The name of the prod config file (overrides properties stored in the normal config file)
DIRS_FROM_ROOT = 1			            # How many directories away this script is from the root


def get_root_path() -> Path:
    path = Path(__file__)

    for _ in range(DIRS_FROM_ROOT + 1):  # the '+ 1' includes this script in the path
        path = path.parent

    return path


def store_json(data: dict, path: Path):
    ## Make sure parents exist (if necessary) so the json can be stored
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_json(path: Path) -> dict:
    with open(path) as fd:
        return json.load(fd)


def load_json_jsonc(path: Path) -> dict:
    if (path.suffix == ".json"):
        return load_json(path)

    if (path.suffix == ".jsonc"):
        return JsoncParser.parse_file(path)

    raise RuntimeError(f"Unable to process path with extension {path.suffix}, must be either .json or .jsonc")


def _build_json_jsonc_config_path(path: Path, config_name: str) -> Path:
    json_path = path / f"{config_name}.json"
    if (json_path.exists()):
        return json_path

    jsonc_path = path / f"{config_name}.jsonc"
    if (jsonc_path.exists()):
        return jsonc_path

    return None


def load_config(directory_path: Path = None) -> dict:
    '''
    Parses one or more JSON (or JSONC) configuration files to build a dictionary with proper precedence for configuring the program
    :param directory_path: Optional path to load configuration files from. If None, then the program's root (cwd/..) will be searched.
    :type directory_path: Path, optional
    :return: A dictionary containing key-value pairs for use in configuring parts of the program.
    :rtype: dictionary
    '''

    path = directory_path or get_root_path()
    config = {}

    ## Load base config
    config_path = _build_json_jsonc_config_path(path, CONFIG_NAME)
    if (config_path is not None):
        config = load_json_jsonc(config_path)

    ## Override the config values if the prod config file exists.
    prod_config_path = _build_json_jsonc_config_path(path, PROD_CONFIG_NAME)
    if (prod_config_path is not None):
        prod_config = load_json_jsonc(prod_config_path)
        for key, value in prod_config.items():
            config[key] = value

    ## Override the config values if the dev config file exists.
    dev_config_path = _build_json_jsonc_config_path(path, DEV_CONFIG_NAME)
    if (dev_config_path is not None):
        dev_config = load_json_jsonc(dev_config_path)
        for key, value in dev_config.items():
            config[key] = value

    return config


def initialize_logging(logger):
    config = load_config()

    FORMAT = "%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(FORMAT)
    logging.basicConfig(format=FORMAT)

    log_level = str(config.get("log_level", "DEBUG"))
    if (log_level == "DEBUG"):
        logger.setLevel(logging.DEBUG)
    elif (log_level == "INFO"):
        logger.setLevel(logging.INFO)
    elif (log_level == "WARNING"):
        logger.setLevel(logging.WARNING)
    elif (log_level == "ERROR"):
        logger.setLevel(logging.ERROR)
    elif (log_level == "CRITICAL"):
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.DEBUG)

    ## Get the directory containing the logs and make sure it exists, creating it if it doesn't
    log_path = config.get("log_path")
    if (log_path):
        log_path = Path(log_path)
    else:
        log_path = Path.joinpath(get_root_path(), 'logs')

    log_path.mkdir(parents=True, exist_ok=True)    # Basically a mkdir -p $log_path
    log_file_name = f"{CONFIG.get('name', 'service')}.log"
    log_file = Path(log_path, log_file_name)    # Build the true path to the log file

    ## Windows has an issue with overwriting old logs (from the previous day, or older) automatically so just delete
    ## them. This is hacky, but I only use Windows for development so it's not a big deal.
    removed_previous_logs = False
    if ('nt' in os.name and log_file.exists()):
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
        now = datetime.datetime.now()
        if (last_modified.day != now.day):
            os.remove(log_file)
            removed_previous_logs = True

    ## Setup and add the timed rotating log handler to the logger
    backup_count = config.get("log_backup_count", 7)    # Store a week's logs then start overwriting them
    log_handler = TimedRotatingFileHandler(str(log_file), when='midnight', interval=1, backupCount=backup_count)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    ## With the new logger set up, let the user know if the previously used log file was removed.
    if (removed_previous_logs):
        logger.info("Removed previous log file.")

    return logger


## Load configuration to aid in logging setup
CONFIG = load_config()
