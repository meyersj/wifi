import unicodecsv as csv

import requests

oui_database = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"
csv_output = "oui_lookup.csv"


def runner(endpoint, output):
    with open(output, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        res = requests.get(endpoint)
        for row in iter(res.text.splitlines()):
            row = row.strip()
            if row.startswith("#"):
                continue
            fields = row.split("\t")
            if len(fields) >= 2:
                prefix = fields[0].strip()
                manuf = fields[1][0:8].strip()
                if len(prefix) == 8 and manuf:
                    try:
                        writer.writerow([prefix, manuf])
                    except Exception as e:
                        pass

def main():
    runner(oui_database, csv_output)


if __name__ == "__main__":
    main()

