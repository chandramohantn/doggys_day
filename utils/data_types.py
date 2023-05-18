import enum


class BreedTypes(enum.IntEnum):
    breed_1 = 1
    breed_2 = 2
    breed_3 = 3
    breed_4 = 4
    breed_5 = 5


class GenderTypes(enum.IntEnum):
    male = 1
    female = 2
    hybrid = 3


class IntEnum(db.TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    impl = db.Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)
