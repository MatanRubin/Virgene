import json
from jsonschema import validate
from os import path
from os import listdir
import pytest

from myvim.common_defs import FEATURES_DIR
from myvim.common_defs import SRC_DIR


def _load_json_path(json_path: str):
    with open(json_path) as json_file:
        return json.load(json_file)

def _find_feature_paths():
    return [path.join(FEATURES_DIR, x) for x in listdir(FEATURES_DIR)]


@pytest.mark.parametrize("feature_path", _find_feature_paths())
def test_validate_feature_schema(feature_path):
    feature_schema = _load_json_path(path.join(SRC_DIR, 'feature_schema.json'))
    feature = _load_json_path(feature_path)
    validate(feature, feature_schema)
