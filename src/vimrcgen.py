"""Vimrc Generator

Usage:
  vimrcgen.py generate -i <input_json> [-o <output_file>]
  vimrcgen.py default-config [-o <output_file>]
  vimrcgen.py (-h | --help)
  vimrcgen.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from datetime import datetime
from os import path
import json
from json import JSONEncoder
import sys
from docopt import docopt
from functional import seq

SRC_DIR = path.abspath(path.dirname(__file__))

class Config:

    def __init__(self):
        self.date_created = str(datetime.now())
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)

    @staticmethod
    def from_json(config_json):
        date_created = config_json["date_created"]
        features_json = config_json["features"]
        config = Config()
        features = [Feature.from_meta_json(x) for x in features_json]
        for feature in features:
            config.add_feature(feature)
        return config


class ConfigMgr:

    def __init__(self):
        pass

    def load_config_path(self, config_path):
        with open(config_path) as config_file:
            config_json = json.load(config_file)
        self.config = Config.from_json(config_json)


    @staticmethod
    def read_json(json_path):
        with open(json_path) as json_file:
            return json.load(json_file)


    @staticmethod
    def generate(input_path, output_path=None):
        abs_input_path = path.join(SRC_DIR, '..', input_path)
        with open(abs_input_path) as input_file:
            input_json = json.load(input_file)
        config = Config.from_json(input_json)
        templates = [path.join(SRC_DIR, x.template_path) for x in config.features]
        output_file = open(output_path, 'w') if output_path is not None else sys.stdout
        for template_path in templates:
            with open(template_path) as template_file:
                output_file.write(template_file.read())
        output_file.close()



    @classmethod
    def get_default_config(cls):
        installed_features = cls.read_installed_features()
        config = Config()
        for feature in installed_features:
            config.add_feature(feature)
        return config

    @staticmethod
    def write_config(config, output_path):
        if output_path is None:
            print(json.dumps(config, cls=MyEncoder, indent=4))
        else:
            with open(output_path, 'w') as output_file:
                output_file.write(json.dumps(config, cls=MyEncoder, indent=4))

    @classmethod
    def default_config(cls, output_path=None):
        config = cls.get_default_config()
        cls.write_config(config, output_path)


    @staticmethod
    def read_installed_features():
        # TODO recursively find all meta files
        meta_files = [
            'metas/emacs_bindings_insert_mode.json',
            'metas/disable_arrow_keys.json',
        ]
        return seq(meta_files).map(lambda x: path.join(SRC_DIR, x))\
            .map(lambda x: Feature.from_meta_path(x))\
            .filter(lambda x: x.installed == True)\
            .to_list()


class MyEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__


class Feature:

    def __init__(self, name, short_description,
                 detailed_description, default_value, enabled,
                 category, notes, popularity, advanced, installed,
                 identifier, template_path, meta_path):
        self.name = name
        self.short_description = short_description
        self.detailed_description = detailed_description
        self.default_value = default_value
        self.enabled = enabled
        self.category = category
        self.notes = notes
        self.popularity = popularity
        self.advanced = advanced
        self.installed = installed
        self.identifier = identifier
        self.template_path = template_path
        self.meta_path = meta_path

    @staticmethod
    def from_meta_json(meta_json):
        return Feature(meta_json["name"], meta_json["short_description"],
                       meta_json["detailed_description"],
                       meta_json["default_value"], meta_json["enabled"],
                       meta_json["category"], meta_json["notes"],
                       meta_json["popularity"], meta_json["advanced"],
                       meta_json["installed"], meta_json["identifier"],
                       meta_json["template_path"],
                       meta_json["meta_path"])


    @staticmethod
    def from_meta_path(meta_path):
        with open(meta_path) as meta_file:
            meta_json = json.load(meta_file)

        return Feature.from_meta_json(meta_json)

    def generate(self):
        with open(self._template_path) as template_file:
            return template_file.read()

    @staticmethod
    def as_feature():
        pass


def test_feature():
    # feature = Feature("emacs_integration", "none", "long desc", True, True,
    #                   "plugins", "N/A", 10, True, True, "emacs",
    #                   "templates/emacs_bindings_insert_mode.j2",
    #                   "metas/emacs_bindings_insert_mode.json")
    feature = Feature.from_meta_path("metas/emacs_bindings_insert_mode.json")
    print(json.dumps(feature, indent=4, cls=MyEncoder))

def test_config():
    config = Config()
    feature1 = Feature.from_meta_path("metas/emacs_bindings_insert_mode.json")
    feature2 = Feature.from_meta_path("metas/disable_arrow_keys.json")
    config.add_feature(feature1)
    config.add_feature(feature2)
    print(json.dumps(config, indent=4, cls=MyEncoder))

if __name__ == '__main__':
    args = docopt(__doc__, version='vimrcgen 0.1')

    if args['default-config']:
        ConfigMgr.default_config(args['<output_file>'])
    elif args['generate']:
        ConfigMgr.generate(args['<input_json>'], args['<output_file>'])