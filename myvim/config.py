from myvim.feature_decoder import FeatureDecoder


class Config:

    def __init__(self):
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)

    @staticmethod
    def from_json(config_json):
        features_json = config_json["features"]
        config = Config()
        for feature_json in features_json:
            feature = FeatureDecoder.decode(feature_json)
            config.add_feature(feature)
        return config
