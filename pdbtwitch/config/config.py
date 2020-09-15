"""
This module is responsible for Setting and loading environments.
"""
import logging
import os
import toml

_logger = logging.getLogger("peeringdb")


class Environment:
    """Environment class for loading and maintaining the config variables """

    def __init__(self):
        """
        env: dict keeping track of all the variables.
        config: dict loaded from the Toml config
        """
        self.config = self._config_loader()
        self.env = self._load_env()

    def _load_env(self):
        env = {}
        env['asn'] = self.config.get('config').get('asn')
        env['asn_api'] = self.config.get('query').get('asn_api')
        env['net_api'] = self.config.get('query').get('net_api')
        return env


    @staticmethod
    def _config_loader():
        """
        Finds the location of the config.toml.
        :return:
        """
        _root_dir = os.path.abspath(os.path.dirname(__file__))
        try:
            loc = os.path.join(_root_dir, '..', 'data')
            with open(os.path.join(loc, "config.toml")) as source:
                return toml.load(source)
        except IOError:
            raise ValueError("config.toml file not found.")


environment = Environment()
