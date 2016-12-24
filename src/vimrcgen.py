"""Vimrc Generator

Usage:
  vimrcgen.py generate -i <input_json> [-o <output_file>]
  vimrcgen.py config-template_path
  vimrcgen.py (-h | --help)
  vimrcgen.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from os import path
import json
from json import JSONEncoder
from pprint import pprint
from docopt import docopt
from functional import seq

SRC_DIR = path.abspath(path.dirname(__file__))

def read_json(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)

def generate(input_json):
    pass


def gen_config_json():
    return {"features": [x.to_json() for x in read_installed_metas()]}



def read_installed_metas():
    # TODO recursively find all meta files
    meta_files = [
        'metas/emacs_bindings_insert_mode.json',
        'metas/disable_arrow_keys.json',
    ]
    return seq(meta_files).map(lambda x: path.join(SRC_DIR, x))\
        .map(lambda x: Feature.from_meta_file(x))\
        .filter(lambda x: x._installed == True)\
        .to_list()

class Feature(object):

    def __init__(self, name, short_description,
                 detailed_description, default_value, enabled,
                 category, notes, popularity, advanced, installed,
                 identifier, template_path, meta_path):
        self._name = name
        self._short_description = short_description
        self._detailed_description = detailed_description
        self._default_value = default_value
        self._enabled = enabled
        self._category = category
        self._notes = notes
        self._popularity = popularity
        self._advanced = advanced
        self._installed = installed
        self._identifier = identifier
        self._template_path = template_path
        self._meta_path = meta_path

    @staticmethod
    def from_meta_file(meta_path):
        with open(meta_path) as meta_file:
            meta_json = json.load(meta_file)

        return Feature(meta_json["name"], meta_json["short_description"],
                       meta_json["detailed_description"],
                       meta_json["default_value"], meta_json["enabled"],
                       meta_json["category"], meta_json["notes"],
                       meta_json["popularity"], meta_json["advanced"],
                       meta_json["installed"], meta_json["identifier"],
                       meta_json["template"], meta_path)

    def to_json(self):
        return self.__dict__

    def generate(self):
        with open(self._template_path) as template_file:
            return template_file.read()

if __name__ == '__main__':
    # arguments = docopt(__doc__, version='Naval Fate 2.0')
    # if arguments['config-template_path']:
    #     config_template()
    # elif arguments['generate']:
    #     generate(arguments['input_json'])
    config_json = gen_config_json()
    out_path = path.join(SRC_DIR, '../output.json')
    with open(out_path, 'w') as out_file:
        out_file.write(json.dumps(config_json, indent=4, sort_keys=True))
