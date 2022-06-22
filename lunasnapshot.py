import json
from multiprocessing.dummy import Pool
import tqdm
from pathlib import Path

from utils.rpc import w3
from utils.constants import *

txs = []
contract = w3.eth.contract


def getContract(address, abi=ERC20_ABI):
    return w3.eth.contract(
        address=w3.toChecksumAddress(address),
        abi=abi,
    )


def getTransfer(contract, blocks):
    events = contract.events.Transfer.createFilter(
        fromBlock=blocks[0], toBlock=blocks[1]
    )
    return events.get_all_entries()


def decodeTransferEvents(events):
    for event in events:
        block = event["blockNumber"]
        args = event["args"]

        txs.append(
            {
                "block": block,
                "from": args["from"],
                "to": args["to"],
                "amount": int(args["value"]),
            }
        )


def save(file, dic):
    with open(file, "w") as f:
        json.dump(dic, f)


def getAndDecodeTransfers(blocks):
    for retries in range(MAX_RETRY + 1):
        try:
            decodeTransferEvents(getTransfer(contract, blocks))
            break
        except Exception as e:
            if retries == MAX_RETRY:
                raise Exception("Too many retries, exiting")
            print("{} blocks failed for {}, retrying...".format(blocks, e))
            pass


def queryEvents():
    with Pool(128) as pool:
        with tqdm.tqdm(total=len(queue)) as pBar:
            for _ in pool.imap(getAndDecodeTransfers, queue):
                pBar.update()


pairContracts = {
    key: getContract(address, abi=PAIR_ABI) for key, address in pairs.items()
}


queue = [
    (i, i + NB_BLOCK - 1)
    for i in range(START_BLOCK, max(PRE_ATTACK_BLOCK, POST_ATTACK_BLOCK), NB_BLOCK)
]

Path("json/pairs").mkdir(parents=True, exist_ok=True)
for name in pairContracts.keys():
    print(name)

    contract = pairContracts[name]

    queryEvents()

    save("json/pairs/{}.json".format(name), txs)

    txs = []
