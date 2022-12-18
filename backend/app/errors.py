

class DomainError(Exception):
    pass


class OutdatedRevisionError(DomainError):
    def __init__(self, passed_revision: int, actual_revision: int):
        self.got = passed_revision
        self.actual = actual_revision
        super().__init__(f'outdated revision: {self.got}, actual revision: {self.actual}')
