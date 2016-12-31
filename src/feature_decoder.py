import json
from src.plugin_feature import PluginFeature
from src.snippet_feature import SnippetFeature
from src.builtin_feature import BuiltinFeature


class FeatureDecoder:

    @staticmethod
    def decode(meta_json):
        constructors = {
            "Plugin": PluginFeature.from_meta_json,
            "Snippet": SnippetFeature.from_meta_json,
            "Builtin": BuiltinFeature.from_meta_json,
        }

        feature_ctor = constructors[meta_json["feature_type"]]
        return feature_ctor(meta_json)

    @staticmethod
    def decode_from_path(meta_path):
        with open(meta_path) as meta_file:
            meta_json = json.load(meta_file)
        return FeatureDecoder.decode(meta_json)