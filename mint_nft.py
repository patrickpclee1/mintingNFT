from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from eth_account.messages import encode_defunct
import secrets

# Step 1: Connect to Avalanche Fuji Testnet
FUJI_RPC_URL = "https://api.avax-test.network/ext/bc/C/rpc"
w3 = Web3(Web3.HTTPProvider(FUJI_RPC_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Step 2: Define the NFT contract ABI and address
contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
contract_abi = [
    # Replace with the full ABI provided to you
]
nft_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Step 3: Generate a new account and get testnet AVAX (done via faucet)
private_key = secrets.token_hex(32)
account = Account.from_key(private_key)
print(f"Generated account address: {account.address}")

# Step 4: Mint an NFT using the 'claim' function
nonce = w3.eth.getTransactionCount(account.address)
random_nonce = secrets.token_bytes(32)
tx = nft_contract.functions.claim(random_nonce).buildTransaction({
    'chainId': 43113,
    'gas': 300000,
    'gasPrice': w3.toWei('30', 'gwei'),
    'nonce': nonce,
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(f"Transaction receipt: {tx_receipt}")

# Step 5: Complete the signChallenge function in verify.py
def signChallenge(challenge: bytes) -> bytes:
    message = encode_defunct(text=challenge.decode('utf-8'))
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)
    return signed_message.signature

# Step 6: Verify ownership of the NFT
token_id = 0  # replace with your actual token ID
owner = nft_contract.functions.ownerOf(token_id).call()
print(f"Owner of token ID {token_id} is {owner}")

# Test the signChallenge function
challenge = b'TestChallenge'
signature = signChallenge(challenge)
print(f"Signed challenge: {signature}")
