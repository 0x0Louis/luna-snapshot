import json

# This should be changed to a private RPC that doesn't have rate limit
AVAX_RPC = "https://api.avax.network/ext/bc/C/rpc"

# The last block where none of the token existed
START_BLOCK = 8_536_961
PRE_ATTACK_BLOCK = 14_390_889
POST_ATTACK_BLOCK = 15_208_591

MAX_RETRY = 10
NB_BLOCK = 512
assert NB_BLOCK <= 2048

ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"
MCJV3_ADDRESS = "0x188bED1968b795d5c9022F6a0bb5931Ac4c18F00"

with open("utils/abi/pair_abi.json", "r") as f:
    PAIR_ABI = json.load(f)


with open("utils/abi/erc20.json", "r") as f:
    ERC20_ABI = json.load(f)

tokens = {
    "LUNA.wh": "0x70928e5b188def72817b7775f0bf6325968e563b",
    "UST.wh": "0xb599c3590F42f8F995ECfa0f85D2980B76862fc1",
    "LUNA.axl": "0x120AD3e5A7c796349e591F1570D9f7980F4eA9cb",
    "UST.axl": "0x260Bbf5698121EB85e7a74f2E45E16Ce762EbE11",
}
pairs = {
    "AVAX-UST.axl": "0x7BF98BD74E19AD8eB5e14076140Ee0103F8F872B",
    "USDC.e-UST.axl": "0xA3A029224857bF467E896523E268a5fc005Ce810",
    "AVAX-UST.wh": "0xeCD6D33555183Bc82264dbC8bebd77A1f02e421E",
    "LUNA.wh-USDC.e": "0x1A0a84dD6E388d977E7B3C0683325Cc58c644E94",
    "LUNA.wh-AVAX": "0xb6fb8Efd0fF5f919d664d49AE750eBe97717C447",
    "LUNA.wh-LUNA.axl": "0x58AD9Dc1c478EC3066c5A71E76e3F9ca8Dc18e21",
    "LUNA.wh-USDC": "0xab95968130bc097b7db8bE769F6172271404cdc7",
    "LUNA.axl-AVAX": "0xdfa0484fbdea70e5e5fa323e314b1274b476c886",
    "LUNA.axl-USDC.e": "0x10cba3727b5b310e9d55b9aea51f04bc6642df98",
    "LUNA.axl-USDt": "0xbbd21be655343bd50eaeb34edcb9c256cf8da3a8",
    "LUNA.axl-USDC": "0x44454e44d8cb8edfbda1750a160448531eb54fc4",
    "LUNA.axl-UST.axl": "0x60db63d557290852bf40f4bfe513c16b8d4877fd",
    "UST.wh-USDC": "0x0a02fc4ad3ad1d3f4c4da8f492907e74cf056017",
    "UST.wh-UST.axl": "0xf98a9c62a1327f5349a9ceaebe26db54c908f0d4",
    "UST.wh-USDC.e": "0x20f095efbe01fada0c53196ca7a05d48e5ec3af5",
    "UST.wh-DAI.e": "0x7383904adf50bdb1106d73af3548d514ac3d1a9f",
    "UST.wh-USDT.e": "0xad91b5771f99ce3d196f9ce40fae2ef1028d74b6",
    "UST.axl-USDC": "0x52d11615659f8229b439179ade36e3833d450654",
    "UST.axl-USDT.e": "0xcfbe608de55e4869867aa0ab5777e65b55f52ce4",
    "UST.axl-USDC.e": "0xa3a029224857bf467e896523e268a5fc005ce810",
}
