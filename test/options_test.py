import pytest
import json
from src.options import BooleanOption
from src.options import ChoiceOption
from src.options import KeymapOption
from src.options import OptionDecoder
from src.default_encoder import DefaultEncoder


def test_boolean_option_set():
    bool_opt = BooleanOption("my_bool_opt", True, "stam")
    bool_opt.set_value(False)
    assert bool_opt.value is False


def test_choice_option_set():
    choice_opt = ChoiceOption("choice option", "A", "choose A,B,C",
                              ["A", "B", "C"])
    choice_opt.set_value("B")
    assert choice_opt.value == "B"


def test_boolean_option_set_bad_value():
    bool_opt = BooleanOption("my_bool_opt", True, "stam")
    with pytest.raises(ValueError):
        bool_opt.set_value("bad value")


def test_choice_option_set_bad_value():
    choice_opt = ChoiceOption("choice option", "A", "choose A,B,C",
                              ["A", "B", "C"])
    with pytest.raises(ValueError):
        choice_opt.set_value("D")

def test_boolean_option_bad_default_value():
    with pytest.raises(ValueError):
        bool_opt = BooleanOption("my_bool_opt", "bad default", "stam")


def test_choice_option_bad_default_value():
    with pytest.raises(ValueError):
        choice_opt = ChoiceOption("choice option", "bad default", "choose A,B,C",
                                  ["A", "B", "C"])

def test_bool_encode_decode():
    bool_opt = BooleanOption("bool opt", True, "bool for encode")
    encoded = json.dumps(bool_opt, cls=DefaultEncoder)
    decoded = OptionDecoder.from_json(json.loads(encoded))
    assert bool_opt == decoded

def test_choice_encode_decode():
    choice_opt = ChoiceOption("choice opt", "A", "bool for encode", ("A", "B"))
    encoded = json.dumps(choice_opt, cls=DefaultEncoder)
    decoded = OptionDecoder.from_json(json.loads(encoded))
    assert choice_opt == decoded
