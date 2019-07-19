from typing import List, Sequence, Set, Any, Union


class PytestTestRunner(object):
    """Runs pytest to discover and run tests."""

    def __init__(self, verbosity: int = 1, failfast: bool = False, keepdb: bool = False, **kwargs: Any) -> None:
        self.verbosity = verbosity
        self.failfast = failfast
        self.keepdb = keepdb

    def run_tests(self, test_labels: Union[Sequence[str], Set[str]]) -> int:
        """Run pytest and return the exitcode. labels = str, List, Tuple, set | not dict
        It translates some of Django's test command option to pytest's.
        """
        import pytest

        argv: List[str] = []
        if self.verbosity == 0:
            argv.append('--quiet')
        if self.verbosity == 2:
            argv.append('--verbose')
        if self.verbosity == 3:
            argv.append('-vv')
        if self.failfast:
            argv.append('--exitfirst')
        if self.keepdb:
            argv.append('--reuse-db')

        if isinstance(test_labels, str):
            argv.append(test_labels)
        elif isinstance(test_labels, (list, tuple, set)):
            argv.extend(test_labels)
        else:
            raise TypeError("Additional test argument labels must be strings or sequence/set of strings")

        tested: int = pytest.main(argv)  # run the tests
        return tested
