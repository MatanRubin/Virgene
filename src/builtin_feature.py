from os import path
import json
from src.common_defs import SRC_DIR
from src.feature_base import FeatureBase


class BuiltinFeature(FeatureBase):

    def __init__(self, name, feature_type, description, default_value, enabled,
                 category, installed, template):
        super().__init__(name, feature_type, description, default_value,
                         enabled, category, installed)
        self.template = template
        # TODO possibly add link to Vim documentation

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

    @staticmethod
    def from_meta_json(meta_json):
        return BuiltinFeature(meta_json["name"], meta_json["feature_type"],
                              meta_json["description"],
                              meta_json["default_value"], meta_json["enabled"],
                              meta_json["category"],
                              meta_json["installed"],
                              meta_json["template"])


    @staticmethod
    def from_meta_path(meta_path):
        with open(path.join(SRC_DIR, 'metas', meta_path)) as meta_file:
            meta_json = json.load(meta_file)

        return SnippetFeature.from_meta_json(meta_json)