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
    def _valid_entry(entry: dict[str, str]) -> bool:
        for key, value in entry.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False
        return True

    @staticmethod
    def _format_entry(entry: dict[str, str]) -> str:
        level = entry.get("log_level")
        message = entry.get("log_message")
        return f"{level}: {message}"

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

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]
        self._store([self._format_entry(entry) for entry in entries])


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    numeric = NumericProcessor()
    print(f"  Trying to validate input '42': {numeric.validate(42)}")
    print(f"  Trying to validate input 'Hello': {numeric.validate('Hello')}")

    print("  Test invalid ingestion of string 'foo' without validation:")
    try:
        numeric.ingest("foo")
    except ValueError as error:
        print(f"  Got exception: {error}")

    numbers: list[int | float] = [1, 2, 3, 4, 5]
    print(f"  Processing data: {numbers}")
    numeric.ingest(numbers)
    print("  Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"  Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(f"  Trying to validate input 'Hello': {text.validate('Hello')}")
    print(f"  Trying to validate input '42': {text.validate(42)}")
    words = ["Hello", "Nexus", "World"]
    print(f"  Processing data: {words}")
    text.ingest(words)
    print("  Extracting 1 value...")
    rank, value = text.output()
    print(f"  Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    valid_log = {
        "log_level": "NOTICE",
        "log_message": "Connection to server",
    }
    print(f"  Trying to validate input {valid_log}: {log.validate(valid_log)}")
    print(f"  Trying to validate input 'Hello': {log.validate('Hello')}")
    logs = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"  Processing data: {logs}")
    log.ingest(logs)
    print("  Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"  Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
