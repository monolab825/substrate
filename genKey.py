import subprocess
from dotenv import load_dotenv
import os

def generate_private_key_from_mnemonic(mnemonic):
    command = f'subkey inspect "{mnemonic}" --scheme sr25519'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    print(output)
    if "Secret seed" in output:
        private_key = output.split(": ")[1]
        return private_key
    else:
        return None

# Example usage:
load_dotenv()
mnemonic_seed = os.environ.get('seed')
print(mnemonic_seed)
private_key = generate_private_key_from_mnemonic(mnemonic_seed)
print("Private Key:", private_key)
