import json

import pytest

from virgene.default_encoder import DefaultEncoder
from virgene.options import BooleanOption
from virgene.options import ChoiceOption
from virgene.options import MultipleSelectionOption
from virgene.options import OptionDecoder


def test_boolean_option_set():
    bool_opt = BooleanOption("my_bool_opt", "my_bool_opt", True, None,
                             "bool opt")
    bool_opt.set_value(False)
    assert bool_opt.value is False


def test_choice_option_set():
    choice_opt = ChoiceOption("choice option", "choice option", "A", None,
                              "choice opt", ["A", "B", "C"])
    choice_opt.set_value("B")
    assert choice_opt.value == "B"


def test_boolean_option_set_bad_value():
    bool_opt = BooleanOption("my_bool_opt", "my_bool_opt", True, None,
                             "bool opt")
    with pytest.raises(ValueError):
        bool_opt.set_value("bad value")


def test_choice_option_set_bad_value():
    choice_opt = ChoiceOption("choice option", "choice option", "A", None,
                              "choice opt", ["A", "B", "C"])
    with pytest.raises(ValueError):
        choice_opt.set_value("D")


def test_boolean_option_bad_default_value():
    with pytest.raises(ValueError):
        BooleanOption("my_bool_opt", "my_bool_opt", "bad default", None,
                      "bool opt")


def test_choice_option_bad_default_value():
    with pytest.raises(ValueError):
        ChoiceOption("choice option", "choice option", "D", None, "choice opt",
                     ["A", "B", "C"])


def test_bool_encode_decode():
    bool_opt = BooleanOption("my_bool_opt", "my_bool_opt", True, None,
                             "bool opt")
    encoded = json.dumps(bool_opt, cls=DefaultEncoder)
    decoded = OptionDecoder.from_json(json.loads(encoded))
    assert bool_opt == decoded


def test_choice_encode_decode():
    choice_opt = ChoiceOption("choice option", "choice option", "A", None,
                              "choice opt", ["A", "B", "C"])
    encoded = json.dumps(choice_opt, cls=DefaultEncoder)
    decoded = OptionDecoder.from_json(json.loads(encoded))
    assert choice_opt == decoded


def test_multiple_selection_encode_decode():
    ms_opt = MultipleSelectionOption("MS option", "MS option",
                                     ("A", "B"), None, "MS opt",
                                     ["A", "B", "C"])
    encoded = json.dumps(ms_opt, cls=DefaultEncoder)
    decoded = OptionDecoder.from_json(json.loads(encoded))
    assert ms_opt == decoded
