from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algokit_utils import ApplicationClient, OnSchemaBreak, OnUpdate
from pathlib import Path
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.account import address_from_private_key
from dotenv import load_dotenv, set_key
import os

load_dotenv()

algod_token = ''
algod_address = 'https://testnet-api.4160.nodely.dev'
algod_client = AlgodClient(algod_token, algod_address)

app_spec = Path(__file__).parent / 'getAlgoPriceContract.arc32.json'

private_key = os.getenv('pk')
signer = AccountTransactionSigner(private_key)

address = address_from_private_key(private_key)

params = algod_client.suggested_params()

indexer_token = ''
indexer_address = 'https://testnet-idx.4160.nodely.dev'
indexer_client = IndexerClient(indexer_token, indexer_address)

app_client = ApplicationClient(
    algod_client=algod_client,
    app_spec=app_spec,
    signer=signer,
    sender=address,
    suggested_params=params,
    creator=address,
    indexer_client=indexer_client
)

app_id = app_client.deploy().app.app_id
#app_id = app_client.deploy(on_schema_break=OnSchemaBreak.AppendApp, on_update=OnUpdate.AppendApp).app.app_id

print(app_id)
set_key('.env', key_to_set='app_id', value_to_set=str(app_id))
