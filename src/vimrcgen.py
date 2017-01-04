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
from src.plugin_feature import PluginFeature
from src.feature_base import FeatureBase
from src.common_defs import *
from src.feature_decoder import FeatureDecoder


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
            feature = FeatureDecoder.decode(feature_json)
            config.add_feature(feature)
        return config


class ConfigMgr:

    def __init__(self):
        self.jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader('src', 'templates'),
            trim_blocks=True,
            lstrip_blocks=True,
            line_statement_prefix='%',
            line_comment_prefix='##'
        )
        self.config = None

    def load_config_path(self, config_path):
        with open(config_path) as config_file:
            config_json = json.load(config_file)
        self.config = Config.from_json(config_json)

    @staticmethod
    def read_json(json_path):
        with open(json_path) as json_file:
            return json.load(json_file)

    # XXX this is convenient but not very good
    def get_template(self, template_string_or_path):
        if path.exists(path.join(TEMPLATES_DIR, template_string_or_path)):
            template = self.jinja_env.get_template(template_string_or_path)
        else:
            template = jinja2.Template(template_string_or_path)
        return template

    def generate(self, input_path, output_path=None):
        with open(input_path) as input_file:
            input_json = json.load(input_file)
        config = Config.from_json(input_json)
        # template = env.get_template('vimrc.j2')
        # print(template.render(configuration=config))


        features_by_type = seq(config.features) \
            .group_by(lambda x: x.feature_type) \
            .group_by_key() \
            .to_dict()

        snippet_features = features_by_type["Snippet"][0]
        plugin_features = features_by_type["Plugin"][0]
        builtin_features = features_by_type["Builtin"][0]

        # TODO can probably write this in a single block
        snippets = []
        plugins = []
        plugin_configurations = []
        builtins = []

        for feature in config.features:
            template = self.get_template(feature.template)
            if feature.feature_type == "Snippet":
                snippets.append(template.render(snippet=feature))
            if feature.feature_type == "Plugin":
                feature.realize_options()
                plugins.append(feature)
                options = {x.name: x.value for x in feature.options}
                plugin_configurations.append(template.render(plugin=feature, options=options))
            if feature.feature_type == "Builtin":
                builtins.append(template.render(builtin=feature))

        vimrc_template = self.jinja_env.get_template("vimrc_template.j2")
        print(vimrc_template.render(snippets=snippets, plugins=plugin_features, plugin_configurations=plugin_configurations, builtins=builtins, has_plugins=True))

    @staticmethod
    def get_default_config():
        installed_features = ConfigMgr.read_installed_features()
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

    @staticmethod
    def default_config(output_path=None):
        config = ConfigMgr.get_default_config()
        ConfigMgr.write_config(config, output_path)


    @staticmethod
    def read_installed_features():
        meta_files = os.listdir(METAS_DIR)
        return seq(meta_files).map(lambda x: path.join(METAS_DIR, x))\
            .map(lambda x: FeatureDecoder.decode_from_path(x))\
            .filter(lambda x: x.installed == True)\
            .to_list()

    def generate_plugin_configurations(self, plugin_jsons):
        return seq(plugin_jsons) \
            .map(lambda plugin_json: (plugin_json, self.jinja_env.get_template(plugin_json.template_path))) \
            .map(lambda plugin_json, template: template.render(plugin=plugin_json)) \
            .to_list()


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