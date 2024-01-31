from typing import Protocol, Any
from .result import HandleResult


class Handler(Protocol):
    def handle(
            self,
            callback:  Any,
            greedy:    bool,
            composer: 'Handler'
    ) -> HandleResult:
        ...


class HandleContext:
    def __init__(
        self,
        handler=None,
        callback=None,
        binding=None,
        composer=None,
        greedy=False
    ):
        self._handler = handler
        self._callback = callback
        self._binding = binding
        self._composer = composer
        self._greedy = greedy

    @property
    def handler(self):
        return self._handler

    @property
    def callback(self):
        return self._callback

    @property
    def binding(self):
        return self._binding

    @property
    def composer(self):
        return self._composer

    @property
    def greedy(self):
        return self._greedy
