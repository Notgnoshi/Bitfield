#!/usr/bin/env python3
import unittest


def runtests(processes=4):
    """
        Run Bitfield's unit tests. Will run the tests in parallel if the `concurrencytest` library
        is installed. Will run serially otherwise.
    """
    # Discover all tests in the current directory that are prefixed with `test`. Also discovers
    # the doctests loaded by defining a load_tests(...) function in the module __init__.py
    loader = unittest.TestLoader()
    doctest_suite = loader.discover('.', pattern='test*.py')
    runner = unittest.runner.TextTestRunner()

    try:
        from concurrencytest import ConcurrentTestSuite, fork_for_tests
        concurrent_doctest_suite = ConcurrentTestSuite(doctest_suite, fork_for_tests(processes))
        runner.run(concurrent_doctest_suite)
    except ImportError:
        runner.run(doctest_suite)

    # Prevent calling sys.exit() just in case the user is running the tests from an interpreter.
    unittest.main(exit=False)


if __name__ == '__main__':
    runtests()
