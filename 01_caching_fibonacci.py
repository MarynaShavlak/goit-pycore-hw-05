def caching_fibonacci():
    """
    Returns a Fibonacci function with caching using closure
    :param cache: The cache to store the calculated Fibonacci numbers
    :return function: The Fibonacci function with caching
    """
    cache = {}
    def fibonacci(n):
        # Return the result from the cache if it exists
        if n in cache:
            return cache[n]

            # Base cases for n = 0 and n = 1
        if n <= 1:
            return n

        cache[n] = fibonacci(n-1) + fibonacci(n-2)
        return cache[n]

    return fibonacci

if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(10))  # prints 55
    print(fib(15))  # prints 610
