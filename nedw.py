import pandas as pd
import asyncio
from substrateinterface import SubstrateInterface

# Initialize the SubstrateInterface
substrate = SubstrateInterface(url="wss://turing-rpc.avail.so/ws")

# Define an asynchronous function to query the total stake for a validator account
async def get_total_stake_async(validator_account):
    print(validator_account)
    result = await substrate.query("Staking", "ErasStakersOverview", ["31", validator_account])
    print(result)
    if result is None or result.value is None:
        return None 
    return result.value.get("total")

# Define a function to apply the asynchronous function to each row in the DataFrame
async def apply_async(func, series):
    results = []
    for item in series:
        result = await func(item)
        results.append(result)
    return results

# Sample DataFrame
data = {'Validator': ['5C869t2dWzmmYkE8NT1oocuEEdwqNnAm2XhvnuHcavNUcTTT'],
        'EraPoints': [860]}
df = pd.DataFrame(data)

# Apply the asynchronous function to each row and add the result as a new column
results = asyncio.run(apply_async(get_total_stake_async, df['Validator']))
df['TotalStake'] = results

# Print the updated DataFrame
print(df)
