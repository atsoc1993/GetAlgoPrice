# Overview
The files in this repository contains a method for fetching the price of Algorand by querying the local state of the ALGO/USDC Tinyman pool against the Tinyman router application.

One example shows fetching the price off-chain, and the other on-chain via smart contract logic.

The same logic can be applied via smart contract by using the AppLocal opcode.

The app ID in the .env can be used on testing and is active

## Deploying your own version of the contract on mainnet or testnet by obtaining TEAL + arc files
Use `algokit compile py get_algo_price_algopy.py --output-arc56` after installing algokit in this project directory, then use deploy.py to deploy your own contract.

## Warning
*This algosdk implementations in this repository are outdated and uses the deprecated ApplicationClient that is far more robust in the new algokit_utils versions*
