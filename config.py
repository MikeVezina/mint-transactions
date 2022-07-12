import os
import secret
from dotenv import load_dotenv

load_dotenv(verbose=True)


project = os.environ["PROJECT"]
dataset = os.environ["DATASET"]

transactions_table = project + '.' + dataset + '.' + os.environ["TRANSACTIONS_TABLE"]
accounts_table = project + '.' + dataset + '.' + os.environ["ACCOUNTS_TABLE"]

# Load secrets from env if testing
token_secret = os.environ.get("MINT_TOKEN_SECRET")
username = os.environ.get("MINT_USERNAME")
password = os.environ.get("MINT_PASSWORD")

# Load secrets
if not token_secret:
    token_secret = secret.access_secret_version(project, 'mint-token', os.environ.get("MINT_TOKEN_VERSION"))

if not username:
    username = secret.access_secret_version(project, 'mint-username', os.environ.get("MINT_USERNAME_VERSION"))

if not password:
    password = secret.access_secret_version(project, 'mint-password', os.environ.get("MINT_PASSWORD_VERSION"))

if not token_secret or not username or not password:
    raise RuntimeError("Failed to load credentials for mint")

print("Configuration loaded.")
