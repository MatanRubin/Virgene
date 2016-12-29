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
import os
import sys
from docopt import docopt
from functional import seq
import jinja2
from src.default_encoder import DefaultEncoder
from src.snippet_feature import SnippetFeature
from src.common_defs import *

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
        for feature_json in features_json:
            if feature_json["feature_type"] == "Snippet":
                feature = SnippetFeature.from_meta_json(feature_json)
                config.add_feature(feature)
            # TODO add here other types of features
            # TODO consider extracting to FeatureDecoder helper class
        return config


class ConfigMgr:

    def __init__(self):
        self.jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader('src', 'templates'),
            trim_blocks=True,
            lstrip_blocks=True,
            line_statement_prefix='%',
            line_comment_prefix='#'
        )

    def load_config_path(self, config_path):
        with open(config_path) as config_file:
            config_json = json.load(config_file)
        self.config = Config.from_json(config_json)


    @staticmethod
    def read_json(json_path):
        with open(json_path) as json_file:
            return json.load(json_file)


    def generate(self, input_path, output_path=None):
        with open(input_path) as input_file:
            input_json = json.load(input_file)
        config = Config.from_json(input_json)
        # template = env.get_template('vimrc.j2')
        # print(template.render(configuration=config))

        # handling just snippets for now
        snippets = []
        for feature in config.features:
            template = self.jinja_env.get_template(feature.template)
            snippets.append(template.render())
        vimrc_template = self.jinja_env.get_template("vimrc_template.j2")
        print(vimrc_template.render(snippets=snippets, plugins=[], has_plugins=False))
        exit(0)

        plugin_configurations = ConfigMgr.generate_plugin_configurations()
        template = self.jinja_env.get_template('ultisnips.j2')
        ultisnips_plugin = [x for x in config.features if x.name == "UltiSnips"][0]
        print(template.render(plugin=ultisnips_plugin))

        template = self.jinja_env.get_template('ctrlp.j2')
        ctrl_plugin = [x for x in config.features if x.name == "CtrlP"][0]
        print(template.render(plugin=ctrl_plugin))
        exit(0)

        templates = [path.join(TEMPLATES_DIR, x.template_path) for x in config.features]
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
            print(json.dumps(config, cls=DefaultEncoder, indent=4))
        else:
            with open(output_path, 'w') as output_file:
                output_file.write(json.dumps(config, cls=DefaultEncoder, indent=4))

    @classmethod
    def default_config(cls, output_path=None):
        config = cls.get_default_config()
        cls.write_config(config, output_path)


    @staticmethod
    def read_installed_features():
        meta_files = os.listdir(METAS_DIR)
        return seq(meta_files).map(lambda x: path.join(METAS_DIR, x))\
            .map(lambda x: SnippetFeature.from_meta_path(x))\
            .filter(lambda x: x.installed == True)\
            .to_list()

    def generate_plugin_configurations(self, plugin_jsons):
        return seq(plugin_jsons) \
            .map(lambda plugin_json: (plugin_json, self.jinja_env.get_template(plugin_json.template_path))) \
            .map(lambda plugin_json, template: template.render(plugin=plugin_json)) \
            .to_list()


class Option:
    
    def __init__(self, name, description, default_value, value):
        self.name = name
        self.description = description
        self.default_value = default_value
        self.value = value


    @staticmethod
    def from_meta_json(meta_json):
        return Option(meta_json["name"], meta_json["description"],
                       meta_json["default_value"], meta_json["value"])


    @staticmethod
    def from_meta_path(meta_path):
        with open(meta_path) as meta_file:
            meta_json = json.load(meta_file)

        return Option.from_meta_json(meta_json)


# TODO have this function as a helper function in each Feature class and
# add to the tests automatic verification of all metas
def verify_meta_json_schemas():
    fields = [
        "name",
        "description",
        "default_value",
        "enabled",
        "category",
        "installed",
        "template_path",
        "template",
        "vundle_installation",
        "options",
    ]

    for meta_path in os.listdir('./metas/'):
        with open(path.join(METAS_DIR, meta_path)) as meta_file:
            meta = json.load(meta_file)
        if seq(meta.keys()).map(lambda x: x not in fields).any():
            print("meta file '{}' has redundant fields".format(meta_path))
        if seq(fields).map(lambda x: x not in meta.keys()).any():
            print("meta file '{}' is missing fields".format(meta_path))


if __name__ == '__main__':
    # verify_meta_json_schemas()
    # exit(0)
    generate_default_vimrc_test()
    exit(0)
    args = docopt(__doc__, version='vimrcgen 0.1')

    if args['default-config']:
        ConfigMgr.default_config(args['<output_file>'])
    elif args['generate']:
        ConfigMgr.generate(args['<input_json>'], args['<output_file>'])

# TODO:
# 0. Finish cleaning up jsons.
# 1. Split code into files
# 2. Make Feature a base class and then inherit into BuiltinFeature, PluginFeature, SnippetFeature, etc
# 3. Think about how to generate the actual vimrc...