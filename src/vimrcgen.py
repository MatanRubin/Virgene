"""Vimrc Generator

Usage:
  vimrcgen.py generate -i <input_json> [-o <output_file>]
  vimrcgen.py config-template
  vimrcgen.py (-h | --help)
  vimrcgen.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from os import path
import json
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
    metas = read_installed_metas()
    by_groups = seq(metas).group_by(lambda x: x["user facing"]["category"])\
    .to_dict()

    output = {}
    for group in by_groups:
        output_options = []
        for option in by_groups[group]:
            output_options.append({option["user facing"]["name"]: option["user facing"]["default value"]})
        output[group] = output_options
    return json.dumps(output)


def read_installed_metas():
    # TODO recursively find all meta files
    meta_files = [
        'metas/emacs_bindings_insert_mode.json',
        'metas/disable_arrow_keys.json',
    ]
    return seq(meta_files).map(lambda x: path.join(SRC_DIR, x))\
        .map(lambda x: read_json(x))\
        .filter(lambda x: x["internal"]["installed"] == True)\
        .to_list()


if __name__ == '__main__':
    # arguments = docopt(__doc__, version='Naval Fate 2.0')
    # if arguments['config-template']:
    #     config_template()
    # elif arguments['generate']:
    #     generate(arguments['input_json'])
    config_json = gen_config_json()
    out_path = path.join(SRC_DIR, '../output.json')
    # with open(out_path, 'w') as out_file:
    #     out_file.write(
    print(json.dumps(json.loads(config_json), indent=4))