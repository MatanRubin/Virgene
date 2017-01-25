from os import path
import json
from typing import List

from myvim.common_defs import FEATURES_DIR
from myvim.options import BooleanOption


class FeatureBase:

    def __init__(self, name, identifier, feature_type, description,
                 default_value, enabled, category, installed, options: List):
        self.name = name
        self.identifier = identifier
        self.feature_type = feature_type
        self.description = description
        self.default_value = default_value
        self.enabled = enabled
        self.category = category
        self.installed = installed
        self.options =  options
        if "enabled" not in [x.identifier for x in options]:
            self.options.insert(0, BooleanOption(name + " Enabled", "enabled",
                                                 False, None, "Enable " + name))

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
               "default_value=%r, enabled=%r, category=%r, installed=%r)" % \
               (self.name, self.feature_type, self.description,
                self.default_value, self.enabled,
                self.category, self.installed)

    @staticmethod
    def from_feature_json(feature_json):
        return FeatureBase(feature_json["name"],
                           feature_json["identifier"],
                           feature_json["feature_type"],
                           feature_json["description"],
                           feature_json["default_value"],
                           feature_json["enabled"],
                           feature_json["category"],
                           feature_json["installed"],
                           [])

    @staticmethod
    def from_feature_path(feature_path):
        with open(path.join(FEATURES_DIR, feature_path)) as feature_file:
            feature_json = json.load(feature_file)

        return FeatureBase.from_feature_json(feature_json)

    def apply_config(self, feature_config: dict):
        pass
