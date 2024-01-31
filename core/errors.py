from typing import Tuple


class MultipleErrors(Exception):
    def __init__(self, *errors: Exception):
        self._errors = self._flatten_errors(errors)

    @property
    def errors(self) -> Tuple[Exception, ...]:
        return self._errors

    @staticmethod
    def combine(*exceptions: Exception) -> Exception | None:
        flattened_exceptions = MultipleErrors._flatten_errors(exceptions)
        if len(flattened_exceptions) == 0:
            return None
        elif len(flattened_exceptions) == 1:
            return flattened_exceptions[0]
        else:
            return MultipleErrors(*flattened_exceptions)

    def __add__(self, other: Exception) -> Exception | None:
        return MultipleErrors.combine(self, other)

    def __str__(self) -> str:
        return ', '.join(str(error) for error in self.errors)

    @staticmethod
    def _flatten_errors(errors: Tuple[Exception | None, ...]) -> Tuple[Exception, ...]:
        return tuple(
            error for err in errors if err is not None
            for error in (err.errors if isinstance(err, MultipleErrors) else (err,))
        )
