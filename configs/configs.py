import json
import os
from base64 import b64decode


class Config(object):
    def __init__(self, config):
        self.config = config

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __getitem__(self, item):
        result = self.config[item]
        if isinstance(result, dict) or isinstance(result, list):
            return Config(result)
        return result


configs = Config(json.loads(
    b64decode(os.getenv('CONFIGS').encode())
))
