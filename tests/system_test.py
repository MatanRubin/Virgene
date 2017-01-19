import pytest
import json
from myvim.feature_base import FeatureBase
from myvim.plugin_feature import PluginFeature
from myvim.default_encoder import DefaultEncoder
from myvim.config_mgr import ConfigMgr


@pytest.mark.parametrize("feature_class,feature_feature_path", [
    (FeatureBase, "hlsearch.json"),
    (PluginFeature, "ctrlp.json")
])
def test_feature_encode_decode(feature_class, feature_feature_path):
    feature = feature_class.from_feature_path(feature_feature_path)
    encoded = json.dumps(feature, cls=DefaultEncoder, indent=4)
    decoded_feature = feature_class.from_feature_json(json.loads(encoded))
    assert(feature == decoded_feature)


def test_generate_default_vimrc():
    config_mgr = ConfigMgr()
    default_config = config_mgr.build_default_config()
    vimrc = config_mgr.generate(default_config)
    print(vimrc)
