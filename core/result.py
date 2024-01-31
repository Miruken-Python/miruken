from typing import Callable
from .errors import MultipleErrors


class HandleResult:
    def __init__(self, handled: bool, stop: bool, err: Exception | None):
        self._handled = handled
        self._stop = stop
        self._err = err

    @property
    def handled(self) -> bool:
        return self._handled

    @property
    def stop(self) -> bool:
        return self._stop

    @property
    def is_error(self) -> bool:
        return self._err is not None

    @property
    def error(self) -> Exception | None:
        return self._err

    def with_error(self, err: Exception | None) -> 'HandleResult':
        if err is None:
            return self
        return HandleResult(self._handled, True, err)

    def without_error(self) -> 'HandleResult':
        if self.is_error:
            return HandleResult(self._handled, self._stop, None)
        return self

    def then(self, block: Callable[[], 'HandleResult']) -> 'HandleResult':
        if block is None:
            raise ValueError("block cannot be None")
        if self._stop:
            return self
        else:
            return self.or_(block())

    def then_if(self, condition: bool, block: Callable[[], 'HandleResult']) -> 'HandleResult':
        if block is None:
            raise ValueError("block cannot be None")
        if self._stop or not condition:
            return self
        else:
            return self.or_(block())

    def otherwise(self, block: Callable[[], 'HandleResult']) -> 'HandleResult':
        if block is None:
            raise ValueError("block cannot be None")
        if self._handled or self._stop:
            return self
        else:
            return block()

    def otherwise_if(self, condition: bool, block: Callable[[], 'HandleResult']) -> 'HandleResult':
        if block is None:
            raise ValueError("block cannot be None")
        if self._stop or (self._handled and not condition):
            return self
        else:
            return self.or_(block())

    def or_(self, other: 'HandleResult') -> 'HandleResult':
        err = combine_errors(self, other)
        if self._handled or other._handled:
            if self._stop or other._stop:
                return HANDLED_AND_STOP.with_error(err)
            else:
                return HANDLED.with_error(err)
        else:
            if self._stop or other._stop:
                return NOT_HANDLED_AND_STOP.with_error(err)
            else:
                return NOT_HANDLED.with_error(err)

    def and_(self, other: 'HandleResult') -> 'HandleResult':
        err = combine_errors(self, other)
        if self._handled and other._handled:
            if self._stop or other._stop:
                return HANDLED_AND_STOP.with_error(err)
            else:
                return HANDLED.with_error(err)
        else:
            if self._stop or other._stop:
                return NOT_HANDLED_AND_STOP.with_error(err)
            else:
                return NOT_HANDLED.with_error(err)

    def __eq__(self, other):
        if isinstance(other, HandleResult):
            return (self._handled == other._handled and
                    self._stop == other._stop and
                    self._err == other._err)
        return False

    def __and__(self, other):
        if isinstance(other, HandleResult):
            return self.and_(other)
        else:
            raise TypeError("Unsupported operand type for &: " + str(type(other)))

    def __or__(self, other):
        if isinstance(other, HandleResult):
            return self.or_(other)
        else:
            raise TypeError("Unsupported operand type for |: " + str(type(other)))


def combine_errors(r1: HandleResult, r2: HandleResult) -> Exception | None:
    if r1.error is not None and r2.error is not None:
        return MultipleErrors(r1.error, r2.error)
    elif r1.error is not None:
        return r1.error
    elif r2.error is not None:
        return r2.error
    return None


HANDLED = HandleResult(True, False, None)
HANDLED_AND_STOP = HandleResult(True, True, None)
NOT_HANDLED = HandleResult(False, False, None)
NOT_HANDLED_AND_STOP = HandleResult(False, True, None)
