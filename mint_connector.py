import datetime
import tempfile

# Load chromedriver on path
from os import path

import chromedriver_binary

print("chromedriver loaded at", chromedriver_binary.chromedriver_filename)

from config import username, password
import mintapi
import pandas as pd


class MintConnector:

    def __init__(self, token):
        self.token = token
        self.mint = self.connect_mint()

    def connect_mint(self):
        session_path = path.join(tempfile.gettempdir(), "session")
        print("Chrome session path at", session_path)
        return mintapi.Mint(
            username,  # Email used to log in to Mint
            password,  # Your password used to log in to mint
            mfa_method='soft-token',
            headless=True,
            mfa_token=self.token,
            session_path=session_path,
            use_chromedriver_on_path=True,

            # Wait for accounts sync
            wait_for_sync=True,
            wait_for_sync_timeout=5*60  # This option waits for sync
        )



    def get_transactions_df(self, include_investment=False, start_date=None, end_date=None):
        transactions = self.mint.get_transactions(include_investment, start_date, end_date)
        transactions.loc[(transactions.transaction_type == 'debit'), 'transaction_type'] = 'Expense'
        transactions.loc[(transactions.transaction_type == 'credit'), 'transaction_type'] = 'Income'
        # transactions = transactions[transactions.category != 'credit card payment']
        return transactions

    def get_accounts_df(self):
        accts = self.mint.get_accounts()
        df = pd.DataFrame(accts)
        df['insert_time'] = datetime.datetime.now()
        return df
