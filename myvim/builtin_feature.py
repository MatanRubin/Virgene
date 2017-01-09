from os import path
import json
from .common_defs import SRC_DIR
from .feature_base import FeatureBase


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

    def __repr__(self, *args, **kwargs):
        return "BuiltinFeature(name=%r, feature_type=%r, description=%r, " \
               "default_value=%r, enabled=%r, category=%r, installed=%r, " \
               "template=%r)" % (self.name, self.feature_type, self.description,
                                 self.default_value, self.enabled,
                                 self.category, self.installed, self.template)

    @staticmethod
    def from_feature_json(feature_json):
        return BuiltinFeature(feature_json["name"], feature_json["feature_type"],
                              feature_json["description"],
                              feature_json["default_value"], feature_json["enabled"],
                              feature_json["category"],
                              feature_json["installed"],
                              feature_json["template"])


    @staticmethod
    def from_feature_path(feature_path):
        with open(path.join(SRC_DIR, 'features', feature_path)) as feature_file:
            feature_json = json.load(feature_file)

        return BuiltinFeature.from_feature_json(feature_json)