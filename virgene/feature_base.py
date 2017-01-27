from os import path
import json
from typing import List

import jinja2

from virgene.common_defs import FEATURES_DIR
from virgene.common_defs import TEMPLATES_DIR


class FeatureBase:

    def __init__(self, name, identifier, feature_type, description,
                 enabled, category, installed, template: str, options: List):
        self.name = name
        self.identifier = identifier
        self.feature_type = feature_type
        self.description = description
        self.enabled = enabled
        self.category = category
        self.installed = installed
        self.template = template
        self.options = options
        self._options_dict = {x.identifier: x for x in self.options}

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self, *args, **kwargs):
        return "FeatureBase(name=%r, feature_type=%r, description=%r, " \
               "enabled=%r, category=%r, installed=%r)" % \
               (self.name, self.feature_type, self.description,
                self.enabled, self.category, self.installed)

    @staticmethod
    def from_feature_json(feature_json):
        return FeatureBase(feature_json["name"],
                           feature_json["identifier"],
                           feature_json["feature_type"],
                           feature_json["description"],
                           feature_json["enabled"],
                           feature_json["category"],
                           feature_json["installed"],
                           feature_json["template"],
                           [])

    @staticmethod
    def from_feature_path(feature_path):
        with open(path.join(FEATURES_DIR, feature_path)) as feature_file:
            feature_json = json.load(feature_file)

        return FeatureBase.from_feature_json(feature_json)

    def apply_config(self, feature_config: dict):
        for option_id in feature_config:  # type: str
            if option_id == "enabled":
                enabled = True if feature_config[option_id] == "true" else False
                self.enabled = enabled
            else:
                option = self.get_option(option_id)
                option.set_value(feature_config[option_id])


    def fill_in_defaults(self):
        for option in self.options:
            option.realize()

    def get_options_dict(self):
        return self._options_dict

    def get_template(self):
        if path.exists(path.join(TEMPLATES_DIR, self.template)):
            return self.template
        else:
            return "one_line_feature.j2"

    def render(self, jinja_env: jinja2.Environment):
        self.fill_in_defaults()
        template = jinja_env.get_template(self.get_template())
        return template.render(feature=self, options=self.get_options_dict())

    def is_enabled(self):
        return self.enabled

    def get_option(self, identifier: str):
        return self._options_dict[identifier]

