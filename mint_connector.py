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
            wait_for_sync_timeout=5 * 60  # This option waits for sync
        )

    def get_transactions_df(self, include_investment=False, start_date=None, end_date=None):
        # Max get_transaction_data limit is 100k
        transactions = self.mint.get_transaction_data(include_investment=include_investment, start_date=start_date,
                                                      end_date=end_date, limit=100000)
        df = pd.json_normalize(transactions, sep='_')
        df['insert_time'] = datetime.datetime.now()
        return df

    def get_accounts_df(self):
        # Max acct limit is 5k
        accts = self.mint.get_account_data(limit=5000)
        df = pd.json_normalize(accts, sep='_')
        df['insert_time'] = datetime.datetime.now()
        return df
