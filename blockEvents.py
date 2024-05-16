from substrateinterface import SubstrateInterface
import pandas as pd
from time import sleep
from decimal import Decimal, getcontext,ROUND_HALF_UP
pd.options.display.max_rows = None
pd.options.display.max_columns = None
import os
from tqdm import tqdm
import json

def formatBalance(amount):
    if amount!=0:
        getcontext().prec = 30
        decimalOutput = Decimal(amount)/Decimal(10**18)
        return (decimalOutput)
    else: 
        return 0


def getCurrentEra(substrate):
    result = substrate.query(
        "Staking", "CurrentEra"
    )
    return int(str(result))


def validatorRewards(substrate,era):
    result = substrate.query(
        "Staking", "ErasValidatorReward",[str(era)]
    )
    return result


def createInstance():
    substrate = SubstrateInterface(url="wss://turing-rpc.avail.so/ws")
    # substrate = SubstrateInterface(url="http://164.92.244.46:9944")
    return substrate

def getBlockHash(substrate,number):
    return substrate.get_block_hash(number)



def indexBlock(substrate):
    data = []
    for i in tqdm(range(195795,200116)):
        try:
            events = substrate.get_events(getBlockHash(substrate,i))
            for items in events:
                for item in items['event']:
                    if type(item)==str:
                        callModule = str(item)
                    else:
                        for rows in item:
                            callFunction = str(rows)
                            break
                if callModule!="System":
                    data.append([i,callModule,callFunction])
            
        except:
            continue
            
    df = pd.DataFrame(data,columns=['BlockNumber','CallModule','CallFunction'])
    # print(df)
    if not os.path.exists('blockEvents.csv'):
        df.to_csv('blockEvents.csv',index=False)
    else:
        df.to_csv('blockEvents.csv',mode='a',index=False, header=False)

def main():
    substrate = createInstance()
    for i in range(207,208):
        events = substrate.get_events(getBlockHash(substrate,i))
        for event in events:
            print('\n')
            print(event)
        # print(events[0]['event'][1][1]['dispatch_info']['weight']['ref_time'])
    # indexBlock(substrate)

main()
# substrate = createInstance()
# blockNumb = 4177
# events = substrate.get_events(getBlockHash(substrate,blockNumb))
# data = []
# for items in events:
#     # print(type(items))

#     for item in items['event']:
#         if type(item)==str:
#             callModule = str(item)
#         else:
#             for rows in item:
#                 callFunction = str(rows)
#                 break
#     data.append([blockNumb,callModule,callFunction])
# df = pd.DataFrame(data,columns=['BlockNumber','CallModule','CallFunction'])
# print(df)
        # print(item,type(item))
        
    # print(items['event'])
    # print(items[0]['event']['event_id'])




# extrinsics = substrate.get_extrinsics(block_number=208)
# print(extrinsics)
# extrinsics = substrate.get_extrinsics(getBlockHash(substrate,126))
# print(extrinsics)
# block = substrate.rpc_request("chain_getBlock", ['0x8f7b45224805e9a5d5f625012bc07e8d007aa0e1cec977465e9e6de08bb64a1c'])