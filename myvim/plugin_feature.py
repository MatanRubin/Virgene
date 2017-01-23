from os import path
import json
from myvim.common_defs import FEATURES_DIR
from myvim.feature_base import FeatureBase
from myvim.options import OptionDecoder


class PluginFeature(FeatureBase):

    def __init__(self, name, identifier, feature_type, description,
                 default_value, enabled, category, installed, template,
                 vundle_installation, options):
        super().__init__(name, identifier, feature_type, description, default_value,
                         enabled, category, installed)
        self.template = template
        self.vundle_installation = vundle_installation
        self.options = options
        self._options_by_id = {x.identifier: x for x in options}

    def __repr__(self, *args, **kwargs):
        return "PluginFeature(name=%r, feature_type=%r, description=%r, " \
               "default_value=%r, enabled=%r, category=%r, installed=%r, " \
               "template=%r, vundle_installation=%r, options=%r)" % \
               (self.name, self.feature_type, self.description,
                self.default_value, self.enabled,
                self.category, self.installed, self.template,
                self.vundle_installation, self.options)

    @staticmethod
    def from_feature_json(feature_json):
        if feature_json["feature_type"] != "Plugin":
            raise TypeError(
                "wrong feature_type='{}'".format(feature_json["feature_type"]))

        options = [OptionDecoder.from_json(x)
                   for x in feature_json.get("options", [])]

        return PluginFeature(feature_json["name"],
                             feature_json["identifier"],
                             feature_json["feature_type"],
                             feature_json["description"],
                             feature_json["default_value"],
                             feature_json["enabled"],
                             feature_json["category"],
                             feature_json["installed"],
                             feature_json["template"],
                             feature_json["vundle_installation"],
                             options)

    @staticmethod
    def from_feature_path(feature_path):
        with open(path.join(FEATURES_DIR, feature_path)) as feature_file:
            feature_json = json.load(feature_file)

        return PluginFeature.from_feature_json(feature_json)

    def fill_in_defaults(self):
        for option in self.options:
            option.realize()

    def apply_config(self, feature_config: dict):
        for option_id in feature_config:  # type: dict
            # FIXME decide if enabled is an option or part of feature
            if option_id == "enabled":
                self.enabled = feature_config[option_id]
            else:
                option = self._options_by_id[option_id]
                option.set_value(feature_config[option_id])
