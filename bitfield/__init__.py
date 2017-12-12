from .bitfield import Bitfield


def run_once(func):
    """
        A function decorator to ensure load_tests() is ran only once. Otherwise the test discovery
        will discover the load_tests() functions more than once and add the tests to the test suite.
        run_once runs the wrapped function once, and then on subsequent runs it calls an empty
        function with three arguments that returns the second argument. This is necessary because
        load_tests() takes in the current tests as its second argument and returns the updated
        tests.

        Example:
        >>> @run_once
        ... def f(a, b, c):
        ...     return b + 2
        >>> f(1, 2, 3)
        4
        >>> f(1, 2, 3)
        2
        >>> f(1, 2, 3)
        2
    """

    def pass_through(loader, tests, ignore):
        """Pass through the TestSuite without adding test cases"""
        return tests

    def wrapper(*args, **kwargs):
        """Wraps `func` to ensure it is only called once"""
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)
        # Otherwise return an empty function
        return pass_through(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    tests.addTests(doctest.DocTestSuite('bitfield'))
    tests.addTests(doctest.DocTestSuite('bitfield.bitfield'))
    return tests
