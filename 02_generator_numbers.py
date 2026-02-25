import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:
    """
        Extracts all floating-point numbers from the given text.

        The function searches for decimal numbers that are separated
        by word boundaries and yields them one by one as floats.

        Args:
            text (str): The input text containing potential numeric values.

        Yields:
            float: Each detected floating-point number found in the text.
    """
    pattern = r"\b\d+\.\d+\b"
    for match in re.finditer(pattern, text):
        yield float(match.group())

def sum_profit(text: str, generator_func: Callable[[str], Generator[float, None, None]]) -> float:
    """
       Calculates the total sum of all floating-point numbers
       extracted from the given text.

       The function accepts a generator function responsible for
       extracting numbers and sums all yielded values.

       Args:
           text (str): The input text containing numeric values.
           generator_func (Callable): A function that takes a string
               and returns a generator of floats.

       Returns:
           float: The total sum of all extracted numbers.
       """
    return sum(generator_func(text))

if __name__ == "__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")

