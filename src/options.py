# TODO: need to assert default value is legal

class Option:

    def __init__(self, name, default_value, description):
        self.description = description
        self.name = name
        self.default_value = default_value
        self.value = None

    def realize(self):
        if self.value is None:
            self.value = self.default_value


class BooleanOption(Option):

    def __init__(self, name, default_value, description):
        assert type(default_value) is bool
        super().__init__(name=name, default_value=default_value,
                         description=description)

    def set_value(self, value):
        if type(value) is not bool:
            raise ValueError("BooleanOption set with non bool argument")
        self.value = value

    @staticmethod
    def from_json(option_json):
        return BooleanOption(option_json["name"], option_json["default_value"],
                             option_json["description"])


class ChoiceOption(Option):

    def __init__(self, name, default_value, description, choices):
        if type(choices) not in (list, tuple):
            raise ValueError("choices must be a list/tuple of choices")
        super().__init__(name=name, default_value=default_value,
                         description=description)
        self.choices = tuple(choices)

    def set_value(self, choice):
        if choice not in self.choices:
            raise ValueError("choice '{}' not in choices='{}'"
                             .format(choice, self.choices))
        self.value = choice

    @staticmethod
    def from_json(option_json):
        return ChoiceOption(option_json["name"], option_json["default_value"],
                            option_json["description"], option_json["choices"])


class KeymapOption(Option):

    def __init__(self, name, default_value, description):
        super().__init__(name, default_value, None)

    def set_value(self, value):
        if type(value) is not str:
            raise ValueError("KeymapOption accepts only strings as values")
        self.value = value

    @staticmethod
    def from_json(option_json):
        return KeymapOption(option_json["name"], option_json["default_value"],
                            option_json["description"])

class OptionDecoder:

    @staticmethod
    def from_json(option_json):
        decoders = {
            "Keymap": KeymapOption.from_json,
            "Boolean": BooleanOption.from_json,
            "Choice": ChoiceOption.from_json,
        }
        decoder = option_json["option_type"]
        return decoder(option_json)