from os import path
import json
from src.vimrcgen import SRC_DIR
from src.feature_base import FeatureBase


class PluginFeature(FeatureBase):

    def __init__(self, name, description, default_value, enabled, category,
                 installed, template, vundle_installation, options):
        super().__init__(name, description, default_value, enabled, category,
                 installed, template)
        self.vundle_installation = vundle_installation
        self.options = options

    @staticmethod
    def from_meta_json(meta_json):
        return PluginFeature(meta_json["name"], meta_json["description"],
                             meta_json["default_value"], meta_json["enabled"],
                             meta_json["category"],
                             meta_json["installed"],
                             meta_json["template"],
                             meta_json["vundle_installation"],
                             meta_json["options"])

    @staticmethod
    def from_meta_path(meta_path):
        with open(path.join(SRC_DIR, 'metas', meta_path)) as meta_file:
            meta_json = json.load(meta_file)

        return PluginFeature.from_meta_json(meta_json)
