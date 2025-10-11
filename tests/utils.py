import filecmp
import os
import shutil
import difflib


def compare_or_update_golden(pytestconfig, golden_file_path, actual_output):
    """
    If the --update-golden command line option is present then update the golden file with the
    actual_output, otherwise assert that the content of the file is equal to the actual output.
    """
    # Tell pytest to not show this function but its caller when displaying a failed test
    __tracebackhide__ = True

    # If the --update-golden option was set, update the golden file
    if pytestconfig.getoption("update_golden"):
        with open(golden_file_path, "w") as file:
            file.write(actual_output)
    else:
        # Otherwise, read the golden file and compare it to the actual output
        with open(golden_file_path, "r") as file:
            golden_output = file.read()

        if actual_output != golden_output:
            # Generate a unified diff to show the differences
            diff = difflib.unified_diff(
                golden_output.splitlines(keepends=True),
                actual_output.splitlines(keepends=True),
                fromfile=f"expected ({golden_file_path})",
                tofile="actual output",
                lineterm="",
            )
            diff_text = "".join(diff)

            assert False, f"Output differs from golden file:\n\n{diff_text}"


def compare_or_update_golden_with_path(pytestconfig, golden_file_path, actual_path):
    """
    If the --update-golden command line option is present then overwrite the
    golden file with the actual_path, otherwise assert that the content of
    the file is equal to the content of actual_path.
    """
    # Tell pytest to not show this function but its caller when displaying a failed test
    __tracebackhide__ = True

    assert os.path.exists(actual_path), f"actual file {actual_path} does not exist"
    golden_path_exists = os.path.exists(golden_file_path)
    if golden_path_exists:
        files_are_the_same = filecmp.cmp(golden_file_path, actual_path, shallow=True)
    else:
        files_are_the_same = False

    # If the --update-golden option was set, update the golden file
    if pytestconfig.getoption("update_golden"):
        if not files_are_the_same:
            shutil.copyfile(actual_path, golden_file_path)
    else:
        assert golden_path_exists, f"golden path {golden_file_path} does not exist"
        assert files_are_the_same, (
            f"actual path {actual_path} should have "
            f"the same content as golden file "
            f"{golden_file_path} but does not"
        )
