# Copyright (C) 2011-2015 The python-bitcoinlib developers
# Copyright (C) 2015 The python-altcoinlib developers
#
# This file is part of python-altcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-altcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from altcoin.core import CoreDogeMainParams, CoreDogeTestNetParams, _SelectCoreParams
from altcoin.core import CoreMonaMainParams, CoreMonaTestNetParams
from altcoin.core import CoreLtcMainParams, CoreLtcTestNetParams
from bitcoin.core import b2lx
import bitcoin

# Note that setup.py can break if __init__.py imports any external
# dependencies, as these might not be installed when setup.py runs. In this
# case __version__ could be moved to a separate version.py and imported here.
__version__ = '0.11.0-SNAPSHOT'

# Litecoin main/testnet information  
#
# Ports:
# https://github.com/litecoin-project/litecoin/blob/master-0.8/src/protocol.h#L19
#
# RPC Ports:
# https://github.com/litecoin-project/litecoin/blob/master-0.8/src/bitcoinrpc.cpp#L40
#
# Seeds: 
# https://github.com/litecoin-project/litecoin/blob/master-0.8/src/net.cpp#L1175
#
# Message start:
# https://github.com/litecoin-project/litecoin/blob/master-0.8/src/main.cpp#L3082
# https://github.com/litecoin-project/litecoin/blob/master-0.8/src/main.cpp#L2745 
#
# Base58 prefixes:
# https://github.com/litecoin-project/litecoin/blob/master-0.8/src/base58.h#L275
#
# Proof of work limit:
# https://github.com/litecoin-project/litecoin/blob/master-0.8/src/main.cpp#L39 
#

class LtcMainParams(CoreLtcMainParams):
    MESSAGE_START = b'\xfb\xc0\xb6\xdb'
    DEFAULT_PORT = 9333
    RPC_PORT = 9332 
    DNS_SEEDS = (('litecointools.com','dnsseed.litecointools.com'),
                 ('litecoinpool.org','dnsseed.litecoinpool.org',),
                 ('xurious.com','dnsseed.ltc.xurious.com'),
                 ('koin-project.com','dnsseed.koin-project.com'),
                 ('weminemnc.com','dnsseed.weminemnc.com'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':48,
                       'SCRIPT_ADDR':5,
                       'SECRET_KEY' :176}
    BECH32_HRP = 'ltc'

class LtcTestNetParams(CoreLtcTestNetParams):
    MESSAGE_START = b'\xfc\xc1\xb7\xdc'
    DEFAULT_PORT = 19333 
    RPC_PORT = 19332
    DNS_SEEDS = (('litecointools.com','testnet-seed.litecointools.com'),
                 ('xurious.com','testnet-seed.ltc.xurious.com'), 
                 ('wemine-testnet.com','dnsseed.wemine-testnet.com'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}
    BECH32_HRP = 'tltc'


# Dogecoin main/testnet information  
# 
# See 
# https://github.com/dogecoin/dogecoin/blob/1.8-maint/src/chainparams.cpp
# There is no bech32 support.

class DogeMainParams(CoreDogeMainParams):
    MESSAGE_START = b'\xc0\xc0\xc0\xc0'
    DEFAULT_PORT = 22556
    RPC_PORT = 22555
    DNS_SEEDS = (('dogecoin.com', 'seed.dogecoin.com'),
                 ('mophides.com', 'seed.mophides.com'),
                 ('dglibrary.org', 'seed.dglibrary.org'),
                 ('dogechain.info', 'seed.dogechain.info'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':30,
                       'SCRIPT_ADDR':22,
                       'SECRET_KEY' :158}

class DogeTestNetParams(CoreDogeTestNetParams):
    MESSAGE_START = b'\xfc\xc1\xb7\xdc'
    DEFAULT_PORT = 44556
    RPC_PORT = 44555
    DNS_SEEDS = (('lionservers.de', 'testdoge-seed-static.lionservers.de'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':113,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :241}

# Monacoin main/testnet information
#
# See
# https://github.com/monacoinproject/monacoin/blob/master-0.17/src/chainparams.cpp

class MonaMainParams(CoreMonaMainParams):
    MESSAGE_START = b'\xfb\xc0\xb6\xdb'
    DEFAULT_PORT = 9401
    RPC_PORT = 9402
    DNS_SEEDS = (('monacoin.org', 'seed.monacoin.org'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':50,
                       'SCRIPT_ADDR':5,
                       'SCRIPT_ADDR2':55,
                       'SECRET_KEY' :176,
                       'OLD_SECRET_KEY' :178}
    BECH32_HRP = 'mona'

class MonaTestNetParams(CoreMonaTestNetParams):
    MESSAGE_START = b'\xfb\xd2\xc8\xf1'
    DEFAULT_PORT = 19403
    RPC_PORT = 19402
    DNS_SEEDS = (('monacoin.org', 'testnet-dnsseed.monacoin.org'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SCRIPT_ADDR2':117,
                       'SECRET_KEY' :239,
                       'OLD_SECRET_KEY' :239}
    BECH32_HRP = 'tmona'

available_params = {}

def SelectParams(genesis_block_hash):
    """Select the chain parameters to use

    genesis_block_hash is the hash of block 0, used to uniquely identify chains
    """
    global available_params
    _SelectCoreParams(genesis_block_hash)
    if genesis_block_hash in available_params:
        bitcoin.params = available_params[genesis_block_hash]
    else:
        raise ValueError('Unknown blockchain %r' % genesis_block_hash)

# Initialise the available_params list
for current_params in [
      # Can't use Bitcoin main net injection because python-bitcoinlib
      # doesn't associate the genesis block with its params
      # bitcoin.MainParams(),
      bitcoin.TestNetParams(),
      DogeMainParams(),
      DogeTestNetParams(),
      MonaMainParams(),
      MonaTestNetParams(),
      LtcMainParams(),
      LtcTestNetParams()
  ]:
  available_params[b2lx(current_params.GENESIS_BLOCK.GetHash())] = current_params


__all__ = (
        'LtcMainParams',
        'LtcTestNetParams',
        'MonaMainParams',
        'MonaTestNetParams',
        'DogeMainParams',
        'DogeTestNetParams',
        'SelectParams',
)
