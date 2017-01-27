import json
import os
from os import path
from typing import List
import jinja2

from virgene.common_defs import SRC_DIR, TEMPLATES_DIR, FEATURES_DIR
from virgene.config import Config
from virgene.default_encoder import DefaultEncoder
from virgene.feature_decoder import FeatureDecoder


class ConfigMgr:

    def __init__(self):
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(path.join(SRC_DIR, 'templates')),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
            line_statement_prefix='%',
            line_comment_prefix='##'
        )
        self.config = None

    @staticmethod
    def load_config_path(config_path) -> Config:
        return Config.from_json(ConfigMgr.read_json_path(config_path))

    @staticmethod
    def read_json_path(json_path) -> json:
        with open(json_path) as json_file:
            return json.load(json_file)

    # XXX this is convenient but not very good
    def get_template(self, template_string_or_path) -> jinja2.Template:
        if path.exists(path.join(TEMPLATES_DIR, template_string_or_path)):
            template = self.jinja_env.get_template(template_string_or_path)
        else:
            template = jinja2.Template(template_string_or_path)
        return template

    def generate(self, config: Config) -> str:
        """
        Receives a vimrc configuration object and return a string containing the
        corresponding vimrc file content
        :param config: Config
        """
        snippets = []
        plugins = []
        plugin_configs = []
        builtins = []

        for feature in config.features:
            if not feature.is_enabled():
                continue
            rendered_feature = feature.render(self.jinja_env)
            if feature.feature_type == "Snippet":
                snippets.append(rendered_feature)
            if feature.feature_type == "Plugin":
                plugins.append(feature)
                plugin_configs.append(rendered_feature)
            if feature.feature_type == "Builtin":
                builtins.append(rendered_feature)

        vimrc_template = self.jinja_env.get_template("vimrc_template.j2")
        return vimrc_template.render(snippets=snippets, plugins=plugins,
                                     plugin_configurations=plugin_configs,
                                     builtins=builtins)

    @staticmethod
    def build_default_config() -> Config:
        installed_features = ConfigMgr.read_installed_features()
        config = Config()
        for feature in installed_features:
            config.add_feature(feature)
        return config

    @staticmethod
    def write_config(config: Config, output_path: [str, None]):
        """
        Writes a Config object to file, or to stdout if output_path is None
        :param config: vimrc configuration object
        :param output_path: path to output file
        :return:
        """
        if output_path is None:
            return json.dumps(config, cls=DefaultEncoder, indent=4)
        else:
            with open(output_path, 'w') as output_file:
                output_file.write(
                    json.dumps(config, cls=DefaultEncoder, indent=4))

    @staticmethod
    def write_default_config(output_path=None):
        config = ConfigMgr.build_default_config()
        ConfigMgr.write_config(config, output_path)

    @staticmethod
    def read_installed_features():
        feature_paths = [path.join(FEATURES_DIR, x)
                         for x in os.listdir(FEATURES_DIR)]
        features = [FeatureDecoder.decode_from_path(x) for x in feature_paths]
        return [x for x in features if x.installed]

    def render_plugin_configs(self, plugin_jsons) -> List[str]:
        """
        takes a list of plugin jsons and produces a list of generated templates,
        one per plugin json
        """
        templates = [self.jinja_env.get_template(x.template_path)
                     for x in plugin_jsons]
        return [template.render(plugin=plugin_json)
                for template, plugin_json in zip(templates, plugin_jsons)]
