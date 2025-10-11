"""End-to-end tests for beangulp imports using the PaypalImporter."""

from pathlib import Path
from beancount_paypal import PaypalImporter, lang
import beangulp
from tests.utils import compare_or_update_golden
from click.testing import CliRunner


def test_e2e_english_paypal_import(testdata_dir, golden_dir, pytestconfig):
    """Test end-to-end conversion of English PayPal CSV to Beancount format."""
    input_file = testdata_dir / "input.csv"
    output_file = golden_dir / "output.beancount"

    # Create importer for English CSV
    importer = PaypalImporter(
        email_address="john@example.com",
        account_name="Assets:PayPal",
        checking_account="Assets:Checking",
        commission_account="Expenses:Commission",
        language=lang.en(),
    )

    ingest = beangulp.Ingest([importer], [])

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("input.csv", "w") as f:
            f.write(input_file.read_text())
        result = runner.invoke(
            ingest.cli, ["extract", "input.csv", "--output", "output.beancount"]
        )
        assert result.exit_code == 0
        with open("output.beancount", "r") as f:
            output_text = f.read()

        # The generated .beancount file contains a header line with the
        # filename that changes from test execution to test execution so we
        # need to verify it separately and remove it before comparing the rest.
        expected_header = f"**** {Path.cwd() / 'input.csv'}\n"
        assert expected_header in output_text, (
            f"Expected header '{expected_header}' not found in output"
        )
        output_text = output_text.replace(expected_header, "")

    # Compare or update golden file
    compare_or_update_golden(pytestconfig, output_file, output_text)


def test_e2e_german_paypal_import(testdata_dir, golden_dir, pytestconfig):
    """Test end-to-end conversion of German PayPal CSV to Beancount format."""
    input_file = testdata_dir / "input.csv"
    output_file = golden_dir / "output.beancount"
    output_text = ""

    # Create importer for German CSV
    importer = PaypalImporter(
        email_address="max@example.com",
        account_name="Assets:PayPal",
        checking_account="Assets:Checking",
        commission_account="Expenses:Commission",
        language=lang.de(),
    )

    ingest = beangulp.Ingest([importer], [])

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("input.csv", "w") as f:
            f.write(input_file.read_text())
        result = runner.invoke(
            ingest.cli, ["extract", "input.csv", "--output", "output.beancount"]
        )
        assert result.exit_code == 0
        with open("output.beancount", "r") as f:
            output_text = f.read()

        # The generated .beancount file contains a header line with the
        # filename that changes from test execution to test execution so we
        # need to verify it separately and remove it before comparing the rest.
        expected_header = f"**** {Path.cwd() / 'input.csv'}\n"
        assert expected_header in output_text, (
            f"Expected header '{expected_header}' not found in output"
        )
        output_text = output_text.replace(expected_header, "")

    # Compare or update golden file
    compare_or_update_golden(pytestconfig, output_file, output_text)
