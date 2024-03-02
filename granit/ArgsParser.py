import sys
from configparser import ConfigParser
from pathlib import Path
from granit.utils import mkdir_images_from_dat_path


class ArgsParser:
    def __init__(self, config_path):
        self.config = ConfigParser()
        self.args = []

        self._args = {}

        if not self.config.read(config_path):
            sys.exit("Config not found. Uncorrected path to ini file")
        self.format_args_for_predict()

    def format_args_for_predict(self):

        for key in self.config['DEFAULT']:


            if key == 'source':
                self._args[key] = self.parse_source_path()

            elif key in ('save-txt', 'save-conf',
                         'save-crop', 'hide-labels', 'hide-conf'):
                self._args[key] = self.parse_as_bool_args(key)

            elif key.lower() in ('cf', 'path_for_autolayout'):
                pass
            else:
                self._args[key] = self.parse_as_value(key)

    def parse_source_path(self):
        source_dat = Path(self.config['DEFAULT']['source'])
        err = mkdir_images_from_dat_path(source_dat, self.config['DEFAULT']['CF'])
        if err:
            sys.exit(str(err))

        path = str(source_dat / 'images')
        self.args.append(
            f"--source {path}"
        )
        return path

    def parse_as_bool_args(self, key):
        if self.config['DEFAULT'].getboolean(key):
            self.args.append(f'--{key}')
            return True
        return False

    def parse_as_value(self, key):
        value = self.config['DEFAULT'][key]
        self.args.append(f"--{key} {value}")
        return value

    def get_args(self):
        return self.args

    def by_key(self, key):
        return self.config['DEFAULT'].get(key)
