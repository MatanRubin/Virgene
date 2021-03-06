# TODO: support multiple selection options


class Option:

    def __init__(self, name, identifier, default_value, value, description):
        self.description = description
        self.identifier = identifier
        self.name = name
        self.default_value = default_value
        self.value = value
        self.option_type = "Option"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        return "Option(name=%r, default_value=%r, value=%r, description=%r)" % \
               (self.name, self.default_value, self.value, self.description)

    def realize(self):
        if self.value is None:
            self.value = self.default_value

    def set_value(self, value):
        self.value = value

    @staticmethod
    def from_json(option_json):
        return Option(option_json["name"],
                      option_json["identifier"],
                      option_json["default_value"],
                      option_json.get("value", None),
                      option_json["description"])


class BooleanOption(Option):

    def __init__(self, name, identifier, default_value, value, description):
        if type(default_value) is not bool:
            raise ValueError("default_value not of type bool")
        super().__init__(name=name, identifier=identifier,
                         default_value=default_value, value=value,
                         description=description)
        self.option_type = "Boolean"

    def __repr__(self):
        return "BooleanOption(name=%r, default_value=%r, " \
               "value=%r, description=%r)" % \
               (self.name, self.default_value, self.value, self.description)

    def set_value(self, value):
        if value in ['True', 'true', 'on', 'On']:
            value = True
        if value in ['False', 'false', 'off', 'Off']:
            value = False
        if type(value) is not bool:
            raise ValueError("BooleanOption set with non bool argument")
        self.value = value

    @staticmethod
    def from_json(option_json):
        return BooleanOption(option_json["name"], option_json["identifier"],
                             option_json["default_value"],
                             option_json.get("value", None),
                             option_json["description"])


class ChoiceOption(Option):

    def __init__(self, name, identifier, default_value, value, description,
                 choices):
        if type(choices) not in (list, tuple):
            raise ValueError("choices must be a list/tuple of choices")
        if default_value not in choices:
            raise ValueError("default_value not in choices")
        if value is not None and value not in choices:
            raise ValueError("choice '{}' not in choices='{}'"
                             .format(value, choices))
        super().__init__(name=name, identifier=identifier,
                         default_value=default_value, value=value,
                         description=description)
        self.choices = tuple(choices)
        self.option_type = "Choice"

    def __repr__(self):
        return "ChoiceOption(name=%r, default_value=%r, " \
               "value=%r, description=%r, choices=%r)" % \
               (self.name, self.default_value, self.value, self.description,
                self.choices)

    def set_value(self, choice):
        if choice not in self.choices:
            raise ValueError("choice '{}' not in choices='{}'"
                             .format(choice, self.choices))
        self.value = choice

    @staticmethod
    def from_json(option_json):
        return ChoiceOption(option_json["name"], option_json["identifier"],
                            option_json["default_value"],
                            option_json.get("value", None),
                            option_json["description"],
                            option_json["choices"])


class MultipleSelectionOption(Option):

    def __init__(self, name, identifier, default_value, value,
                 description, choices):
        value = tuple(value) if value else ()
        if type(choices) not in (list, tuple):
            raise ValueError("choices must be a list/tuple of choices")
        if any([x not in choices for x in default_value]):
            raise ValueError("default_value not in choices")
        if value is not None and any([x not in choices for x in value]):
            raise ValueError("choice '{}' not in choices='{}'"
                             .format(value, choices))
        super().__init__(name=name, identifier=identifier,
                         default_value=tuple(default_value),
                         value=value, description=description)
        self.choices = tuple(choices)
        self.option_type = "MultipleSelection"

    def __repr__(self):
        return "MultipleSelectionOption(name=%r, default_value=%r, " \
               "value=%r, description=%r, choices=%r)" % \
               (self.name, self.default_value, self.value, self.description,
                self.choices)

    def set_value(self, selection):
        if type(selection) is not list:
            selection = [selection]
        if any([x not in self.choices for x in selection]):
            raise ValueError("selection {} not in choices='{}'"
                             .format(selection, self.choices))
        self.value = selection

    @staticmethod
    def from_json(option_json):
        return MultipleSelectionOption(option_json["name"],
                                       option_json["identifier"],
                                       option_json["default_value"],
                                       option_json.get("value", None),
                                       option_json["description"],
                                       option_json["choices"])


class KeymapOption(Option):

    def __init__(self, name, identifier, default_value, value, description):
        super().__init__(name, identifier, default_value, value, description)
        self.option_type = "Keymap"

    def __repr__(self):
        return "KeymapOption(name=%r, default_value=%r, " \
               "value=%r, description=%r)" % \
               (self.name, self.default_value, self.value, self.description)

    def set_value(self, value):
        if type(value) is not str:
            raise ValueError("KeymapOption accepts only strings as values")
        self.value = value

    @staticmethod
    def from_json(option_json):
        return KeymapOption(option_json["name"],
                            option_json["identifier"],
                            option_json["default_value"],
                            option_json.get("value", None),
                            option_json["description"])


class NumberOption(Option):

    def __init__(self, name, identifier, default_value, value, description):
        super().__init__(name, identifier, default_value, value, description)
        self.option_type = "Number"

    def __repr__(self):
        return "NumberOption(name=%r, default_value=%r, " \
               "value=%r, description=%r)" % \
               (self.name, self.default_value, self.value, self.description)

    def set_value(self, value):
        try:
            int(value)
        except ValueError:
            raise ValueError("NumberOption accepts only integers as values")
        self.value = value

    @staticmethod
    def from_json(option_json):
        return NumberOption(option_json["name"],
                            option_json["identifier"],
                            option_json["default_value"],
                            option_json.get("value", None),
                            option_json["description"])


class OptionDecoder:

    @staticmethod
    def from_json(option_json):
        decoders = {
            "Option": Option.from_json,
            "Keymap": KeymapOption.from_json,
            "Boolean": BooleanOption.from_json,
            "Choice": ChoiceOption.from_json,
            "MultipleSelection": MultipleSelectionOption.from_json,
            "Number": NumberOption.from_json,
        }
        decoder = decoders[option_json["option_type"]]
        return decoder(option_json)
