from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._items: list[tuple[int, str]] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool: ...

    @abstractmethod
    def ingest(self, data: Any) -> None: ...

    def output(self) -> tuple[int, str]:
        if not self._items:
            raise IndexError("No data available")
        return self._items.pop(0)

    def _store(self, items: list[str]) -> None:
        for item in items:
            self._items.append((self._rank, item))
            self._rank += 1


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, int | float):
            return True
        if isinstance(data, list):
            for d in data:
                if not isinstance(d, int | float):
                    return False
            return True
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            values = data
        else:
            values = [data]
        self._store([str(value) for value in values])


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            for d in data:
                if not isinstance(d, str):
                    return False
            return True
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            values = data
        else:
            values = [data]
        self._store(values)


class LogProcessor(DataProcessor):
    @staticmethod
    def _valid_entry(entry: dict[str, str]):
        for key, value in entry.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False
        return True
    
    @staticmethod
    def _format_entry(entry: dict[str, str]) -> str:
        level = entry.get("log_level")
        message = entry.get("log_message")
        

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return self._valid_entry(data)
        if isinstance(data, list):
            for d in data:
                if not isinstance(d, dict):
                    return False
                if not self._valid_entry(d):
                    return False
            return True
        return False

    def ingest(self, data: dict[str, str]):
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            values = data
        else:
            values = [data]
        self._store(self.)
