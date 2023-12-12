from configparser import ConfigParser
import os


def get_configs_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    settings_dir = os.path.join(current_dir, '..', 'settings')
    conf_file_path = os.path.join(settings_dir, 'configs.cfg')
    return conf_file_path


def read_config(section: str, key: str) -> str:

    path = get_configs_path()
    config = ConfigParser()
    config.read(path)

    if config.has_option(section, key):
        return config.get(section, key)


def write_config(section: str, key: str, value: str):

    path = get_configs_path()
    config = ConfigParser()
    config.read(path)
    if section not in config.sections():
        config.add_section(section)
        config.set(section, key, value)
        with open(path, 'w') as configfile:
            config.write(configfile)
    else:
        config.set(section, key, value)

    with open(path, 'w') as configfile:
        config.write(configfile)
