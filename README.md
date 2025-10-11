# Beancount PayPal Importer

`beancount-paypal` provides an Importer for converting CSV exports of PayPal into the beancount format.

## Installation

### Using uv (recommended)

```sh
uv add git+https://github.com/nils-werner/beancount-paypal.git
```

### Using pip

```sh
pip install git+https://github.com/nils-werner/beancount-paypal.git
```

### For development

```sh
git clone https://github.com/nils-werner/beancount-paypal.git
cd beancount-paypal
uv sync
```

#### Code quality

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```sh
uv run ruff check .     # lint
uv run ruff format .    # format
```

## Usage

### Basic usage

Configure `PaypalImporter` in your importer script, and download your PayPal statements as CSV.

In PayPal you can customize the report fields. If you enable `Transaction Details > Balance`, the
beancount output will be finalized with a `balance` assertion.


```python
from beancount_paypal import PaypalImporter

CONFIG = [
    PaypalImporter(
        'my-paypal-account@gmail.com',
        'Assets:US:PayPal',
        'Assets:US:Checking',
        'Expenses:Financial:Commission',
    )
]
```

### Advanced usage

If you enable additional report fields you can map them into transaction metadata using the
`metadata_map` keyword argument:

```python
from beancount_paypal import PaypalImporter, lang

CONFIG = [
    PaypalImporter(
        'my-paypal-account@gmail.com',
        'Assets:US:PayPal',
        'Assets:US:Checking',
        'Expenses:Financial:Commission',
        language=lang.de(),
        metadata_map={
            "uuid": "Transaktionscode",
            "sender": "Absender E-Mail-Adresse",
            "recipient": "Empfänger E-Mail-Adresse"
        }
    )
]
```
