from substrateinterface import SubstrateInterface,Keypair,KeypairType
from substrateinterface.exceptions import SubstrateRequestException
from dotenv import load_dotenv
import os
import subprocess
import binascii

load_dotenv()

def ss58_to_hex(ss58_public_key):
    command = f'subkey inspect "{ss58_public_key}" --scheme sr25519'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    # print(output)
    if "Public key (SS58)" in output:
        parts = output.split()
        for i, part in enumerate(parts):
            if part == "Public" and parts[i+1] == "key" and parts[i+2] == "(SS58):":
                return parts[i+3]
    return None


substrate = SubstrateInterface(url="wss://turing-rpc.avail.so/ws")
# Define the shortform private key
# privatekey = bytes.fromhex(os.environ.get("privateKey"))
seed = os.environ.get('seed')

# keypair = Keypair.create_from_private_key(privatekey, crypto_type=KeypairType.ECDSA)
# keypair = Keypair.create_from_mnemonic(seed,crypto_type=KeypairType.SR25519)
keypair = Keypair.create_from_uri(seed)

# Form a transaction call
# call = substrate.compose_call(
#     call_module="Staking",
#     call_function="payoutStakers",
#     call_params={
#         "validatorStash": "5DyrSBNDRo6oaW4QPisptTYAoK6fsZovbQoxpE8L8ftCfd1n",
#         "era": 40
#     },
# )
dest = "5He2hnSrFFM15s9k7ha4ksuUS4t4k2Vhcvm2Nrgrb5WC3tHc"
# dest = ss58_to_hex("5He2hnSrFFM15s9k7ha4ksuUS4t4k2Vhcvm2Nrgrb5WC3tHc")
# print(dest)

call = substrate.compose_call(
    call_module="Balances",
    call_function="transfer_keep_alive",
    call_params={
        "dest": str(dest),
        "value": 1 * 10**18,
    },
)
# print(keypair.ss58_address)
# print(keypair.mnemonic)
# print(keypair.ss58_format)
# print(binascii.hexlify(keypair.public_key).decode('utf-8'))
# print(binascii.hexlify(keypair.seed_hex).decode('utf-8'))

# print(call)
# "5GT7HazmxhGQcMrXCDBQzFoisx9LKxVLnyzcFHWTG2eDEdAy"
extrinsic = substrate.create_signed_extrinsic(call = call, keypair=keypair,tip_asset_id=0)
# Submit the extrinsic


print(extrinsic)

# try:
#     receipt = substrate.submit_extrinsic(extrinsic)
#     print(
#         "Extrinsic '{}' sent and included in block '{}'".format(
#             receipt.extrinsic_hash, receipt.block_hash
#         )
#     )
# except SubstrateRequestException as e:
#     print("Failed to send: {}".format(e))

