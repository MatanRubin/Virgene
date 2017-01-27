from os import path
import json
from virgene.common_defs import FEATURES_DIR
from virgene.feature_base import FeatureBase
from virgene.options import OptionDecoder


class PluginFeature(FeatureBase):

    def __init__(self, name, identifier, feature_type, description,
                 enabled, category, installed, template,
                 vundle_installation, options):
        super().__init__(name, identifier, feature_type, description,
                         enabled, category, installed, template, options)
        self.vundle_installation = vundle_installation

    def __repr__(self, *args, **kwargs):
        return "PluginFeature(name=%r, feature_type=%r, description=%r, " \
               "enabled=%r, category=%r, installed=%r, " \
               "template=%r, vundle_installation=%r, options=%r)" % \
               (self.name, self.feature_type, self.description,
                self.enabled, self.category, self.installed, self.template,
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
