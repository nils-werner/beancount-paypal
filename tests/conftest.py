import os
import pathlib

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--update-golden",
        action="store_true",
        help="Update the golden files",
        default=False,
    )


@pytest.fixture
def golden_dir(request: pytest.FixtureRequest) -> pathlib.Path:
    """
    Return the path to the golden directory for the test currently being
    executed. The directory will be created if it does not exist. A golden file
    is a file that contains the output that is expected from some execution so
    the output can be compared to that golden file. It's more convenient than
    embedding large amounts of text or data within the test itself.  Golden
    directory just means a directory containing golden files.

    The location of the golden directory will be:
      - Inside the current test package a directory "golden"
      - Within that directory a directory named like the current test module
      - Within that directory a directory named like the current test function

    For example the golden directory for the test function
    "test_importer_functionality" contained in tests/importers/test_paypal.py
    will be tests/importers/golden/test_paypal/test_importer_functionality/ The
    test can access any file within that directory. Those files must be
    created.

    Note that the test itself is expected to overwrite the content of the files
    when tests are invoked with --update-golden as a convenience for the
    developer (instead of having to manually update all golden files).
    """
    # For this project, we expect test files to be directly in tests/
    # so module.__name__ will be like "tests.test_paypal_importer"
    module_name = request.node.module.__name__
    test_module = module_name.split(".")[-1]  # e.g. "test_paypal_importer"
    test_function = request.node.function.__name__

    golden_dir_path = pathlib.Path(
        os.path.dirname(__file__),
        "golden",
        test_module,
        test_function,
    )
    golden_dir_path.mkdir(exist_ok=True, parents=True)
    return golden_dir_path


@pytest.fixture
def testdata_dir(request: pytest.FixtureRequest) -> pathlib.Path:
    """
    Return the path to the test data directory for any data the test may need.
    The directory will be created if it does not exist.

    The location of the test data directory will be:
      - Inside the current test package a directory "testdata"
      - Within that directory a directory named like the current test module
      - Within that directory a directory named like the current test function

    For example the test data directory for the test function
    "test_importer_functionality" contained in tests/importers/test_paypal.py
    will be tests/importers/testdata/test_paypal/test_importer_functionality/
    The test can access any file within that directory. Those files must be
    created.
    """
    # For this project, we expect test files to be directly in tests/
    # so module.__name__ will be like "tests.test_paypal_importer"
    module_name = request.node.module.__name__
    test_module = module_name.split(".")[-1]  # e.g. "test_paypal_importer"
    test_function = request.node.function.__name__

    testdata_dir_path = pathlib.Path(
        os.path.dirname(__file__),
        "testdata",
        test_module,
        test_function,
    )
    testdata_dir_path.mkdir(exist_ok=True, parents=True)
    return testdata_dir_path
