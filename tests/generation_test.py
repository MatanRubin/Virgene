import jinja2
from os import path

from virgene.common_defs import TEMPLATES_DIR
from virgene.common_defs import FEATURES_DIR
from virgene.builtin_feature import BuiltinFeature
from virgene.plugin_feature import PluginFeature
from virgene.snippet_feature import SnippetFeature

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
    line_statement_prefix='%',
    line_comment_prefix='##'
)


def test_one_line_feature():
    number_path = path.join(FEATURES_DIR, "number.json")
    feature = BuiltinFeature.from_feature_path(number_path)
    output = feature.render(jinja_env)
    assert "Displays lines numbers" in output
    assert "set number" in output
    assert len(output.splitlines()) == 1


def test_plugin_feature():
    ctrlp_path = path.join(FEATURES_DIR, "ctrlp.json")
    feature = PluginFeature.from_feature_path(ctrlp_path)
    output = feature.render(jinja_env)
    assert "CtrlP" in output
    assert "Full path fuzzy" in output
    assert "ctrlp_working_path_mode" in output
    assert len(output.splitlines()) > 1


def test_snippet_feature():
    disable_arrow_keys_path = path.join(FEATURES_DIR, "disable_arrow_keys.json")
    feature = SnippetFeature.from_feature_path(disable_arrow_keys_path)
    output = feature.render(jinja_env)
    assert "Disable arrow keys" in output
    assert "Forces you" in output
    assert "<Up>" in output
    assert "<nop>" in output
    assert len(output.splitlines()) > 1
