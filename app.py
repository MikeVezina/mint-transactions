"""
A sample Hello World server.
"""
# # Load .env before other imports
# import dotenv
# dotenv.load_dotenv()
from datetime import date

import mint_connector as mc
from big_query_connector import BigQueryConnector
from config import token_secret, transactions_table, accounts_table


def get_last_transaction(bq):
    query = f"""
            SELECT MAX(date) as max_date
            FROM `{transactions_table}`
            LIMIT 1
        """

    result_df = bq.query_table(query)

    if result_df.size < 1:
        return None
    else:
        return result_df.iloc[0, 0].date()


def load_mint_transactions():
    print("Connecting to mint")
    mint = mc.MintConnector(token=token_secret)
    print("Connected")

    transactions = mint.get_transactions_df()
    accounts = mint.get_accounts_df()
    bq = BigQueryConnector()

    if transactions.size > 0:
        bq.write_df(transactions_table, df=transactions, overwrite_table=True)
        print("Wrote transactions to table")
    else:
        print("No transactions to write")

    if transactions.size > 0:
        bq.write_df(accounts_table, df=accounts, overwrite_table=False)
        print("Appended accounts")
    else:
        print("No accounts to write")


if __name__ == '__main__':
    load_mint_transactions()
