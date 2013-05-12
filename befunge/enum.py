def enum(**enums):
    """
    from
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    as a stop-gap until PEP 435
    """

    # add a getitem method so that the enumeration is also dict-ish
    class Enum(type):
        def __getitem__(cls, k):
            return cls.__dict__[k]

        def items(cls):
            return cls.__dict__.items()

        def keys(cls):
            return [t for t in cls.__dict__.keys() if not t.startswith('_')]

    return Enum('Enum', (), enums)
