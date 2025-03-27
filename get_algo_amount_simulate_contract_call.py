from algosdk.v2client.algod import AlgodClient
from algokit_utils import ApplicationClient
from pathlib import Path
from algosdk.atomic_transaction_composer import AccountTransactionSigner, AtomicTransactionComposer
from algosdk.v2client.models.simulate_request import SimulateRequest
from algosdk.account import address_from_private_key
import os
from dotenv import load_dotenv

load_dotenv()

algod_token = ''
algod_address = 'https://testnet-api.4160.nodely.dev'
algod_client = AlgodClient(algod_token, algod_address)

app_id = int(os.getenv('app_id'))

app_spec = Path(__file__).parent / 'getAlgoPriceContract.arc32.json'

private_key = os.getenv('pk')
signer = AccountTransactionSigner(private_key)

address = address_from_private_key(private_key)

params = algod_client.suggested_params()


app_client = ApplicationClient(
    algod_client=algod_client,
    app_id=app_id,
    app_spec=app_spec,
    signer=signer,
    sender=address,
    suggested_params=params,
)


atc = AtomicTransactionComposer()

usdc_pool_address = 'UDFWT5DW3X5RZQYXKQEMZ6MRWAEYHWYP7YUAPZKPW6WJK3JH3OZPL7PO2Y' #testnet
tinyman_router = 148607000 #testnet

usdc_amount = 1000

app_client.compose_call(
    atc,
    call_abi_method='getTargetUSDCAmountInAlgo',
    target_usdc=usdc_amount,
    transaction_parameters={
        'accounts': [usdc_pool_address],
        'foreign_apps': [tinyman_router]
    }
)

sim_req = SimulateRequest(txn_groups=atc.build_group())
results = atc.simulate(algod_client, sim_req)

abi_results = [results.abi_results[i].return_value for i in range(len(results.abi_results))]
tx_ids = [results.tx_ids[i] for i in range(len(results.tx_ids))]

print(abi_results[0])
algorand_amount_of_usdc = abi_results[0] / 100
print(f'USDC amount in Algo: {algorand_amount_of_usdc}')
print(f'Tx IDS: {tx_ids}')
