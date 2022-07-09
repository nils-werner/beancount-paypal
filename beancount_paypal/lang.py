from datetime import datetime

class base():
    def identify(self, fields):
        return all(elem in fields for elem in list(self.fields_map.keys())[:-4])  # last 4 keys are optional

    def txn_from_checking(self, data):
        return data == self._from_checking

    def txn_currency_conversion(self, data):
        return data == self._currency_conversion

    def decimal(self, data):
        return data

    def parse_date(self, data):
        return datetime.strptime(data, self._format)

    def normalize_keys(self, row):
        return { self.fields_map.get(k, k):row[k] for k in row }


class en(base):
    fields_map = {
        "Date": "date",
        "Time": "time",
        "TimeZone": "timezone",
        "Name": "name",
        "Type": "txn_type",
        "Status": "status",
        "Currency": "currency",
        "Gross": "gross",
        "Fee": "fee",
        "Net": "net",
        "From Email Address": "from",
        "To Email Address": "to",
        "Transaction ID": "txn_id",
        "Reference Txn ID": "reference_txn_id",
        "Receipt ID": "receipt_id",
        # Optional keys:
        "Item Title": "item_title",
        "Subject": "subject",
        "Note": "note",
        "Balance": "balance",
    }

    metadata_map = {
        "uuid": "Transaction ID",
        "sender": "From Email Address",
        "recipient": "To Email Address",
    }

    _format = "%d/%m/%Y"
    _from_checking = "Bank Deposit to PP Account "
    _currency_conversion = "General Currency Conversion"

    def decimal(self, data):
        return data.replace(".", "").replace(",", ".")


class de(base):
    fields_map = {
        "Datum": "date",
        "Uhrzeit": "time",
        "Zeitzone": "timezone",
        "Name": "name",
        "Typ": "txn_type",
        "Status": "status",
        "Währung": "currency",
        "Brutto": "gross",
        "Gebühr": "fee",
        "Netto": "net",
        "Absender E-Mail-Adresse": "from",
        "Empfänger E-Mail-Adresse": "to",
        "Transaktionscode": "txn_id",
        "Zugehöriger Transaktionscode": "reference_txn_id",
        "Empfangsnummer": "receipt_id",
        # Optional keys:
        "Artikelbezeichnung": "item_title",
        "Betreff": "subject",
        "Hinweis": "note",
        "Guthaben": "balance",
    }

    metadata_map = {
        "uuid": "Transaktionscode",
        "sender": "Absender E-Mail-Adresse",
        "recipient": "Empfänger E-Mail-Adresse",
    }

    _format = "%d.%m.%Y"
    _from_checking = "Bankgutschrift auf PayPal-Konto"
    _currency_conversion = "Allgemeine Währungsumrechnung"

    def decimal(self, data):
        return data.replace(".", "").replace(",", ".")


class fr(base):
    fields_map = {
        "Date": "date",
        "Heure": "time",
        "Fuseau horaire": "timezone",
        "Nom": "name",
        "Type": "txn_type",
        "État": "status",
        "Devise": "currency",
        "Avant commission": "gross",
        "Commission": "fee",
        "Net": "net",
        "De l'adresse email": "from",
        "À l'adresse email": "to",
        "Numéro de transaction": "txn_id",
        "Numéro de la transaction de référence": "reference_txn_id",
        "Numéro de facture": "receipt_id",
        # Optional keys:
        "Titre de l'objet": "item_title",
        "Objet": "subject",
        "Remarque": "note",
        "Solde": "balance",
    }

    metadata_map = {
        "uuid": "Numéro de transaction",
        "sender": "De l'adresse email",
        "recipient": "À l'adresse email",
    }

    _format = "%d/%m/%Y"
    _from_checking = "Virement bancaire sur le compte PayPal"
    _currency_conversion = "Conversion de devise standard"

    def decimal(self, data):
        return data.replace(".", "").replace(",", ".")
