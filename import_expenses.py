import csv
import json
from biyuya.models.expense import ExpenseFactory, Expense
from biyuya.models.account import Account
import arrow


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="csv expenses", metavar="data")

    args = parser.parse_args()
    imported_accounts, imported_expenses = 0, 0

    with open(args.data, newline='', encoding='utf-8') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile)

        for row in reader:
            if not Account.by_name(row['Account']):
                print("Adding new account ", row['Account'])
                Account.add(Account(name=row['Account'], currency=row['Currency']))
                imported_accounts += 1

            doc = {
                'date': arrow.get(row['Date']).datetime,
                'account': row['Account'],
                'amount': row['Amount'],
                'tags': row['Tags'].split(','),
                'notes': row['Notes']
            }

            if row['Month'] and row['Total Months']:
                doc.update({'month': row['Month'], 'total_months': row['Total Months']})

            #print("Adding expense {}".format(json.dumps(ExpenseFactory.build(doc), indent=2)))
            Expense.add(ExpenseFactory.build(doc))
            imported_expenses += 1

    print("Imported {} accounts and {} expenses".format(imported_accounts, imported_expenses))
