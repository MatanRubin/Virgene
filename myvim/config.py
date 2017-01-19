from typing import List

from myvim.feature_decoder import FeatureDecoder


class Config:

    def __init__(self):
        self.features = []
        self._features_by_name = {}

    @staticmethod
    def from_json(config_json):
        features_json = config_json["features"]
        config = Config()
        for feature_json in features_json:
            feature = FeatureDecoder.decode(feature_json)
            config.add_feature(feature)
        return config

    def add_feature(self, feature):
        self.features.append(feature)
        self._features_by_name[feature.name] = feature

    def apply_config(self, config: List[dict]):
        for feature_config in config:  # type: dict
            feature = self._features_by_name[feature_config["name"]]
            feature.apply_config(feature_config)
