from abc import ABC, abstractmethod


class TransformCapability(ABC):
    def __init__(self) -> None:
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> None: ...

    @abstractmethod
    def revert(self) -> None: ...

    def _attack_message(self, normal: str, transformed: str) -> str:
        if self._transformed:
            return transformed
        return normal
