from json import JSONEncoder


class DefaultEncoder(JSONEncoder):

    # Encode only non private members
    def default(self, o):
        return {x: o.__dict__[x] for x in o.__dict__ if not x.startswith('_')}
