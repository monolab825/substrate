from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from substrateinterface.utils.ss58 import ss58_encode
from dotenv import load_dotenv
import os
from decimal import Decimal




def main():
    load_dotenv()
    try:
        # Initialize Substrate interface
        substrate = SubstrateInterface(url="wss://turing-rpc.avail.so/ws")

        # Validate recipient address
        if not substrate.is_valid_ss58_address("5He2hnSrFFM15s9k7ha4ksuUS4t4k2Vhcvm2Nrgrb5WC3tHc"):
            raise ValueError("Invalid Recipient")

        # Load keypair from seed
        keypair = Keypair.create_from_uri(os.environ.get('seed'))

        # Calculate amount in the smallest unit (planck)
        # decimals = substrate.get_metadata()["tokenDecimals"]["token"]
        decimals =18
        amount = int(1 * 10 ** decimals)

        # Get recipient account info
        old_balance = substrate.query(
            module="System",
            storage_function="Account",
            params=['5He2hnSrFFM15s9k7ha4ksuUS4t4k2Vhcvm2Nrgrb5WC3tHc']
        )
        print(f"Balance before the transfer call: {Decimal(str(old_balance['data']['free'])) / 10 ** decimals}")

        # Build and send the transaction
        call = substrate.compose_call(
            call_module='Balances',
            call_function='transfer_keep_alive',
            call_params={
                'dest': '5He2hnSrFFM15s9k7ha4ksuUS4t4k2Vhcvm2Nrgrb5WC3tHc',
                'value': amount
            }
        )
        extrinsic = substrate.create_signed_extrinsic(call=call,keypair=keypair)

        print("Transaction sent. Waiting for finalization...")

        # Wait for the transaction to be finalized
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)

        print(f"Transaction finalized: {receipt.extrinsic_hash}")

        # Get updated recipient account info
        new_balance= substrate.query(
            module="System",
            storage_function="Account",
            params=['5He2hnSrFFM15s9k7ha4ksuUS4t4k2Vhcvm2Nrgrb5WC3tHc']
        )
        print(f"Balance after the transfer call: {Decimal(str(new_balance['data']['free'])) / 10 ** decimals}")

    except SubstrateRequestException as e:
        print(f"Substrate request error: {e}")
        exit(1)
    except ValueError as e:
        print(f"Value error: {e}")
        exit(1)

# Execute the main function
main()
