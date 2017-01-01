import pytest
from src.options import BooleanOption
from src.options import ChoiceOption
from src.options import KeymapOption


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
    bool_opt = BooleanOption("my_bool_opt", "bad value", "stam")
    bool_opt.set_value(False)
    assert bool_opt.value is False


def test_choice_option_set_bad_value():
    choice_opt = ChoiceOption("choice option", "A", "choose A,B,C",
                              ["A", "B", "C"])
    choice_opt.set_value("D")
    assert choice_opt.value == "B"