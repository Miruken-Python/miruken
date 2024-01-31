from typing import Any, Tuple, Protocol
from handler import HandleContext
import asyncio


class Binding(Protocol):
    def key(self) -> Any:
        ...

    def is_strict(self) -> bool:
        ...

    def skip_filters(self) -> bool:
        ...

    def is_async(self) -> bool:
        ...

    def is_exported(self) -> bool:
        ...

    def metadata(self) -> list[Any]:
        ...

    def logical_output_type(self) -> type:
        ...

    def invoke(
            self,
            context:    HandleContext,
            *init_args: Any
    ) -> Tuple[Any, asyncio.Future | None]:
        ...
