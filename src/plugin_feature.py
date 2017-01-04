from os import path
import json
from src.common_defs import METAS_DIR
from src.feature_base import FeatureBase
from src.options import OptionDecoder

class PluginFeature(FeatureBase):

    def __init__(self, name, feature_type, description, default_value, enabled,
                 category, installed, template, vundle_installation, options):
        super().__init__(name, feature_type, description, default_value,
                         enabled, category, installed)
        self.template = template
        self.vundle_installation = vundle_installation
        self.options = options

    @staticmethod
    def from_meta_json(meta_json):
        if meta_json["feature_type"] != "Plugin":
            raise TypeError("wrong feature_type='{}'".format(meta_json["feature_type"]))

        options = [OptionDecoder.from_json(x) for x in meta_json.get("options", [])]

        return PluginFeature(meta_json["name"], meta_json["feature_type"],
                             meta_json["description"],
                             meta_json["default_value"], meta_json["enabled"],
                             meta_json["category"], meta_json["installed"],
                             meta_json["template"],
                             meta_json["vundle_installation"],
                             options)

    @staticmethod
    def from_meta_path(meta_path):
        with open(path.join(METAS_DIR, meta_path)) as meta_file:
            meta_json = json.load(meta_file)

        return PluginFeature.from_meta_json(meta_json)

    def realize_options(self):
        for option in self.options:
            option.realize()
