from algosdk.v2client.algod import AlgodClient
from algosdk.transaction import LogicSigAccount
from base64 import b64decode

algod_token = ''
#algod_address = 'https://testnet-api.4160.nodely.dev' # Testnet
algod_address = 'https://mainnet-api.4160.nodely.dev' # Mainnet
algod_client = AlgodClient(algod_token, algod_address)

POOL_LOGICSIG_TEMPLATE = (
    "BoAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgQBbNQA0ADEYEkQxGYEBEkSBAUM="
)

def get_pool_logicsig(
    validator_app_id: int, asset_a_id: int, asset_b_id: int
) -> LogicSigAccount:
    
    assets = [asset_a_id, asset_b_id]
    asset_1_id = max(assets)
    asset_2_id = min(assets)

    program = bytearray(b64decode(POOL_LOGICSIG_TEMPLATE))
    program[3:11] = validator_app_id.to_bytes(8, "big")
    program[11:19] = asset_1_id.to_bytes(8, "big")
    program[19:27] = asset_2_id.to_bytes(8, "big")
    
    return LogicSigAccount(program)


#TINYMAN_ROUTER = 148607000 # Testnet router
TINYMAN_ROUTER = 1002541853 # Mainnet router

#asset_a = 10458941 # Testnet USDC
asset_a = 31566704 # Mainnet USDC

asset_b = 0 # Algo

logic_sig_account = get_pool_logicsig(TINYMAN_ROUTER, asset_a, asset_b)
pool_address = logic_sig_account.address()

local_states = algod_client.account_application_info(pool_address, TINYMAN_ROUTER)['app-local-state']['key-value']
for state in local_states:
    decoded_state = b64decode(state['key'])
    if decoded_state == b'asset_1_reserves':
        asset_1_reserves = state['value']['uint']
    if decoded_state == b'asset_2_reserves':
        asset_2_reserves = state['value']['uint']

algorand_price = asset_1_reserves / asset_2_reserves
print(algorand_price)
