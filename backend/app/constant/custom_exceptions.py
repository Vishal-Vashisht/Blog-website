class PostNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        self.message = args[0]


class UserExistException(Exception):
    def __init__(self, *args: object) -> None:
        self.messgae = args[0]


class UserDoesNotExistException(Exception):
    def __init__(self, *args: object) -> None:
        self.messgae = args[0]


class InvvalidCredException(Exception):
    def __init__(self, *args: object) -> None:
        self.messgae = args[0]
