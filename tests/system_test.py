import pytest
import json
import jsonschema
from os import path

from myvim.common_defs import SRC_DIR
from myvim.feature_base import FeatureBase
from myvim.plugin_feature import PluginFeature
from myvim.default_encoder import DefaultEncoder
from myvim.config_mgr import ConfigMgr


def _load_json_path(json_path: str):
    with open(json_path) as json_file:
        return json.load(json_file)


@pytest.mark.parametrize("feature_class,feature_feature_path", [
    (FeatureBase, "hlsearch.json"),
    (PluginFeature, "ctrlp.json")
])
def test_feature_encode_decode(feature_class, feature_feature_path):
    feature = feature_class.from_feature_path(feature_feature_path)
    encoded = json.dumps(feature, cls=DefaultEncoder, indent=4)
    decoded_feature_json = json.loads(encoded)
    feature_schema = _load_json_path(path.join(SRC_DIR, 'feature_schema.json'))
    jsonschema.validate(decoded_feature_json, feature_schema)
    decoded_feature = feature_class.from_feature_json(decoded_feature_json)
    assert(feature == decoded_feature)


def test_generate_default_vimrc():
    config_mgr = ConfigMgr()
    default_config = config_mgr.build_default_config()
    vimrc = config_mgr.generate(default_config)
    print(vimrc)
