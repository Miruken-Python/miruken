from typing import Any, Tuple, Protocol
from result import HandleResult
from handler import Handler
from policy import Policy
import asyncio


class Callback(Protocol):
    def key(self) -> Any: ...

    def source(self) -> Any: ...

    def target(self) -> Any: ...

    def target_for_write(self) -> Any: ...

    def policy(self) -> Policy: ...

    def result_count(self) -> int: ...

    def result(self, many: bool) -> Tuple[Any, asyncio.Future | None]: ...

    def set_result(self, result: Any): ...

    def receive_result(
            self,
            result:   Any,
            strict:   bool,
            composer: Handler
    ) -> HandleResult: ...
