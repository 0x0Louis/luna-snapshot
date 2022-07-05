import json
from pathlib import Path

from multiprocessing.dummy import Pool
import tqdm

from utils.constants import *
from utils.rpc import w3


addresses = set()


def save(file, dic):
    with open(file, "w") as f:
        json.dump(dic, f)


def getUniqueAddresses(name):
    with open("json/pairs/{}.json".format(name)) as f:
        dic = json.load(f)
    for data in dic:
        addresses.add(data["from"])
        addresses.add(data["to"])


def call(func: w3.eth.contract):
    return func.call({}, MIDDLE_ATTACK_BLOCK)


ustPairs = {
    name: w3.toChecksumAddress(address)
    for name, address in pairs.items()
    if "ust" in name.lower()
}

ustPairs.pop("LUNA.axl-UST.axl")  # created after MIDDLE_BLOCK

for name in ustPairs:
    getUniqueAddresses(name)

boring_helper = w3.eth.contract(
    address=w3.toChecksumAddress(BORING_HELPER_ADDRESS),
    abi=BORING_HELPER_ABI,
)

ust = w3.eth.contract
balances = {}

pairsInfo = {}

print("init pairs")
for name, address in ustPairs.items():
    print(name)
    pairsInfo[address] = {}

    pair = w3.eth.contract(
        address=w3.toChecksumAddress(address),
        abi=PAIR_ABI,
    )

    pairsInfo[address]["name"] = name
    pairsInfo[address]["totalSupply"] = call(pair.functions.totalSupply())
    reserve0, reserve1, ts = call(pair.functions.getReserves())
    pairsInfo[address][call(pair.functions.token0())] = reserve0
    pairsInfo[address][call(pair.functions.token1())] = reserve1
print(pairsInfo)
print("pairs init done")


def queryBalance(user):
    if user == ADDRESS_ZERO or user in pairs.values():
        return

    for retries in range(MAX_RETRY + 1):
        try:
            dic = dict(
                call(
                    boring_helper.functions.findBalances(
                        user, list([ust.address]) + list(ustPairs.values())
                    )
                )
            )
            balance = 0
            for address, lpAmount in dic.items():
                if ust.address == address:
                    balance += dic[ust.address]
                elif ust.address in pairsInfo[address]:
                    res = pairsInfo[address][ust.address]
                    ts = pairsInfo[address]["totalSupply"]
                    balance += lpAmount * res // ts
            if balance > 0:
                balances[user] = balance
            break
        except Exception as e:
            if retries == MAX_RETRY:
                raise Exception("Too many retries, exiting")
            print("{} balance failed for {}, retrying...".format(user, e))
            pass


def queryBalances():
    with Pool(128) as pool:
        with tqdm.tqdm(total=len(addresses)) as pBar:
            for _ in pool.imap(queryBalance, addresses):
                pBar.update()


# Create path if it doesn't exist yet
Path("json/snapshot/mid-attack").mkdir(parents=True, exist_ok=True)

for name, address in tokens.items():
    if "ust" in name.lower():
        ust = w3.eth.contract(
            address=w3.toChecksumAddress(address),
            abi=ERC20_ABI,
        )
        queryBalances()
        save("json/snapshot/mid-attack/{}.json".format(name), balances)
        balances = {}
