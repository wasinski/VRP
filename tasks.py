from functools import partial

from invoke import task

pprint = partial(print, "-" * 3)

LINE_LENGTH = "79"


@task
def sort_imports(c, check=False):
    """
    Sort imports.
    """
    ISORT_CMD = (
        f"isort cvrp tests tasks.py --recursive --atomic"
        f" --quiet --apply --line-width {LINE_LENGTH}"
    )
    if check:
        result = c.run(ISORT_CMD + " --check")
        if result.stdout.startswith("ERROR"):
            exit(1)
    else:
        c.run(ISORT_CMD)


@task
def format_code(c, check=False):
    """Format code"""
    BLACK_CMD = f"black cvrp tests tasks.py --line-length {LINE_LENGTH}"
    if check:
        result = c.run(BLACK_CMD + " --check")
        if result.return_code != 0:
            exit(1)
    else:
        c.run(BLACK_CMD)


@task
def check_types(c):
    """Static types checking"""
    MYPY_CMD = "mypy cvrp"
    result = c.run(MYPY_CMD)
    if result.return_code != 0:
        exit(1)


@task
def lint(c):
    """Lint code"""
    PYLINT_CMD = "pylint cvrp tests tasks.py"
    c.run(PYLINT_CMD, warn=True)


@task
def test(c):
    """Run tests"""
    PYTEST_CMD = "pytest tests"
    result = c.run(PYTEST_CMD)
    exit(result.return_code)


@task
def precommit(c, check=False):
    """
    Task which should be run before commiting. Invokes formatting and import sorting.

    :param check: decides if it's a full run (with changes), or only a check
    """
    pprint("SORT IMPORTS:")
    sort_imports(c, check)

    pprint("FORMAT CODE:")
    format_code(c, check)

    pprint("TYPE CHECK:")
    check_types(c)

    pprint("LINT:")
    lint(c)


@task
def prepr(c, check=False):
    """
    Task that should be run before submitting PR

    :param check: decides if it's a full run (with changes), or only a check
    """
    pprint("SORT IMPORTS:")
    sort_imports(c, check)

    pprint("FORMAT CODE:")
    format_code(c, check)

    pprint("TYPE CHECK:")
    check_types(c)

    pprint("LINT:")
    lint(c)

    pprint("TEST:")
    test(c)
