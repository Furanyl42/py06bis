from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    name: str

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

    @property
    def total_processed(self) -> int:
        return self._rank

    @property
    def remaining(self) -> int:
        return len(self._items)


class NumericProcessor(DataProcessor):
    name: str = "Numeric Processor"

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
    name: str = "Text Processor"

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
    name: str = "Log Processor"

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


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            target: DataProcessor | None = None
            for processor in self._processors:
                if processor.validate(element):
                    target = processor
                    break
            if target is None:
                print(
                    "DataStream error - Can't process element in "
                    f"stream: {element}"
                )
            else:
                target.ingest(element)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for processor in self._processors:
            print(
                f"{processor.name}: total "
                f"{processor.total_processed} items processed, "
                f"remaining {processor.remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")

    print("\nInitialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    print(f"\nSend first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)

    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    for _ in range(3):
        numeric.output()
    for _ in range(2):
        text.output()
    for _ in range(1):
        log.output()

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
