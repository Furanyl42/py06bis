from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None: ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [value for _, value in data]
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        fields: list[str] = []
        for rank, value in data:
            fields.append(f'"item_{rank}": "{value}"')
        print("JSON Output:")
        print("{" + ", ".join(fields) + "}")


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self._processors:
            items: list[tuple[int, str]] = []
            for _ in range(nb):
                if processor.remaining == 0:
                    break
                items.append(processor.output())
            if items:
                plugin.process_output(items)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")

    print("\nInitialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    first_batch: list[Any] = [
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

    print(f"\nSend first batch of data on stream: {first_batch}")
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    stream.print_processors_stats()

    second_batch: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]

    print(f"\nSend another batch of data: {second_batch}")
    stream.process_stream(second_batch)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
