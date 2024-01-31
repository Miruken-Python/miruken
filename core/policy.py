from typing import Any, Tuple, Protocol
from result import HandleResult
from binding import Binding
from intent import Intent


class Policy(Protocol):
    def is_strict(self) -> bool:
        ...

    def less(self, binding: Binding, other_binding: Binding) -> bool:
        ...

    def variant_key(self, key: Any) -> Tuple[bool, bool]:
        ...

    def matches_key(self, key: Any, other_key: Any, invariant: bool) -> Tuple[bool, bool]:
        ...

    def accept_results(self, results: list[Any]) -> Tuple[Any, HandleResult, list[Intent]]:
        ...
