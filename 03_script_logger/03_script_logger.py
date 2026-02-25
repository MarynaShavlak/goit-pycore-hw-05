import sys
from typing import List, Dict,TypedDict
from collections import Counter

class LogEntry(TypedDict):
    date: str
    time: str
    level: str
    message: str


LogList = List[LogEntry]
LogCounts = Dict[str, int]

def parse_log_line(line: str) -> LogEntry:
    """
    Parses a log line into components:
    date, time, level, message.
    """
    parts = line.strip().split(maxsplit=3)

    if len(parts) < 4:
        raise ValueError(f"Invalid log format: {line}")

    date, time, level, message = parts

    return LogEntry(
        date=date,
        time=time,
        level=level,
        message=message
    )

def load_logs(file_path: str) -> LogList:
    """
    Loads and parses log file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [
                parse_log_line(line)
                for line in file
                if line.strip()
            ]

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")

    except PermissionError:
        raise PermissionError(f"No permission to read '{file_path}'.")

    except OSError as e:
        raise OSError(f"File error: {e}")

def filter_logs_by_level(logs: LogList, level: str) -> LogList:
    """
        Filters logs by logging level.
    """
    level = level.upper()
    return [log for log in logs if log["level"] == level]
    # or different approach can be:
    return list(filter(lambda log: log["level"] == level, logs))

def count_logs_by_level(logs: LogList) -> Counter[str]:
    """
       Counts logs grouped by level using Counter.
     """
    return Counter(log["level"] for log in logs)

def calculate_level_width(counts: LogCounts, header: str) -> int:
    """
    Calculates the width of the 'level' column dynamically.
    """
    longest_level = max((len(level) for level in counts), default=0)
    return max(len(header), longest_level)


def print_table_header(level_header: str, count_header: str, level_width: int) -> None:
    """
    Prints the table header.
    """
    print(f"{level_header:<{level_width}} | {count_header}")
    print(f"{'-' * level_width}-|{'-' * (len(count_header) + 1)}")


def print_table_rows(counts: LogCounts, level_width: int) -> None:
    """
    Prints table rows with sorted log levels.
    """
    for level in sorted(counts):
        print(f"{level:<{level_width}} | {counts[level]}")

def display_log_counts(counts: LogCounts)-> None:
    """
    Displays log statistics as a table.
    """
    header_level = "Рівень логування"
    header_count = "Кількість"

    level_width = calculate_level_width(counts, header_level)

    print_table_header(header_level, header_count, level_width)
    print_table_rows(counts, level_width)

def display_filtered_logs(logs: LogList, level: str) -> None:
    """
    Displays detailed logs for specific level.
    """
    level=level.upper()
    if not logs:
        print(f"\nНемає записів для рівня '{level}'.")
        return

    print(f"\nДеталі логів для рівня '{level}':")

    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python 03_script_logger.py <log_file_path> [log_level]")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        logs = load_logs(file_path)

    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    if len(sys.argv) == 3:
        level = sys.argv[2]
        filtered = filter_logs_by_level(logs, level)
        display_filtered_logs(filtered, level)
    else:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)


if __name__ == "__main__":
    main()