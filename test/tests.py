from os import path
import pytest
import json
from src.feature_base import FeatureBase
from src.plugin_feature import PluginFeature
from src.default_encoder import DefaultEncoder
from src.vimrcgen import ConfigMgr
from src.common_defs import BUILD_DIR

#
# def test_feature_base_encode_decode():
#     feature = FeatureBase(name="test_feature", description="test description",
#                           default_value=True, enabled=True, category="Base",
#                           installed=True, template="./templates/ctrlp.j2")
#     encoded = json.dumps(feature, cls=DefaultEncoder, indent=4)
#     decoded_feature = FeatureBase.from_meta_json(json.loads(encoded))
#     assert(feature == decoded_feature)


@pytest.mark.parametrize("feature_class,feature_meta_path", [
    (FeatureBase, "hlsearch.json"),
    (PluginFeature, "ctrlp.json")
])
def test_feature_encode_decode(feature_class, feature_meta_path):
    feature = feature_class.from_meta_path(feature_meta_path)
    encoded = json.dumps(feature, cls=DefaultEncoder, indent=4)
    decoded_feature = feature_class.from_meta_json(json.loads(encoded))
    assert(feature == decoded_feature)

def test_generate_default_vimrc():
    config_mgr = ConfigMgr()
    test_config_path = path.join(BUILD_DIR, "default.json")
    config_mgr.default_config(test_config_path)
    config_mgr.generate(test_config_path)