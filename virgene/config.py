from typing import Dict
from typing import List

from virgene.feature_decoder import FeatureDecoder


class Config:

    def __init__(self):
        self.features = []
        self._features_by_id = {}

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
        self._features_by_id[feature.identifier] = feature

    def apply_config(self, config):
        for feature_config in config:
            feature = self._features_by_id[feature_config]
            feature.apply_config(config[feature_config])
