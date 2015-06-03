#!/usr/bin/python
import python_sha3
import aes
import os
import sys
import json
import getpass
import pbkdf2 as PBKDF2
from bitcoin import *
import urllib2

from optparse import OptionParser

# Values used by pybitcointools bci.py for blockr network
TESTNET = 'testnet'
MAINNET = 'btc'

SATOSHI_PER_BTC = 10**8

# Arguments
network = TESTNET

if network == TESTNET:
    exodus = 'mvBWJFv8Uc84YEyZKBm8HZQ7qrvmBiH7zR'
    magicbyte = 111
else:
    exodus = ''  # TODO
    magicbyte = 0

satoshiFee = 30000  # 3mBTC fee for the Bitcoin miner

# Option parsing

parser = OptionParser()
parser.add_option('-p', '--password',
                  default=None, dest='pw')
parser.add_option('-s', '--seed',
                  default=None, dest='seed')
parser.add_option('-w', '--wallet',
                  default='btcToEtherWallet.json', dest='wallet')
parser.add_option('-o', '--overwrite',
                  default=False, dest='overwrite')

(options, args) = parser.parse_args()

# Function wrappers


def sha3(x):
    return python_sha3.sha3_256(x).digest()


def pbkdf2(x):
    return PBKDF2._pbkdf2(x, x, 2000)[:16]


# Makes a request to a given URL (first arg) and optional params (second arg)
def make_request(url, data, headers):
    req = urllib2.Request(url, data, headers)
    return urllib2.urlopen(req).read().strip()


# Prefer openssl because it's more well-tested and reviewed; otherwise,
# use pybitcointools' internal ecdsa implementation
try:
    import openssl
except:
    openssl = None


def openssl_tx_sign(tx, priv):
    if len(priv) == 64:
        priv = priv.decode('hex')
    if openssl:
        k = openssl.CKey()
        k.generate(priv)
        u = k.sign(bitcoin.bin_txhash(tx))
        return u.encode('hex')
    else:
        return ecdsa_tx_sign(tx, priv)


def secure_sign(tx, i, priv):
    i = int(i)
    if not re.match('^[0-9a-fA-F]*$', tx):
        return sign(tx.encode('hex'), i, priv).decode('hex')
    if len(priv) <= 33:
        priv = priv.encode('hex')
    pub = privkey_to_pubkey(priv)
    address = pubkey_to_address(pub)
    signing_tx = signature_form(tx, i, mk_pubkey_script(address))
    sig = openssl_tx_sign(signing_tx, priv)
    txobj = deserialize(tx)
    txobj["ins"][i]["script"] = serialize_script([sig, pub])
    return serialize(txobj)


def secure_privtopub(priv):
    if len(priv) == 64:
        return secure_privtopub(priv.decode('hex')).encode('hex')
    if openssl:
        k = openssl.CKey()
        k.generate(priv)
        return k.get_pubkey()
    else:
        return privtopub(priv)


def tryopen(f):
    try:
        assert f
        t = open(f).read()
        try:
            return json.loads(t)
        except:
            raise Exception("Corrupted file: "+f)
    except:
        return None


def eth_privtoaddr(priv):
    pub = encode_pubkey(secure_privtopub(priv), 'bin_electrum')
    return sha3(pub)[12:].encode('hex')


def getseed(encseed, pw, ethaddr):
    seed = aes.decryptData(pw, encseed.decode('hex'))
    ethpriv = sha3(seed)
    if eth_privtoaddr(ethpriv) != ethaddr:
        raise Exception("Ethereum address provided to getseed does not match!")
    return seed


def genwallet(seed, pw):
    encseed = aes.encryptData(pw, seed)
    ethpriv = sha3(seed)
    btcpriv = sha3(seed + '\x01')
    ethaddr = sha3(secure_privtopub(ethpriv)[1:])[12:].encode('hex')
    btcaddr = privkey_to_address(btcpriv, magicbyte)
    return {
        "encseed": encseed.encode('hex'),
        "ethaddr": ethaddr,
        "btcaddr": btcaddr
    }

# etherFeePercent is a string in format xx.xx eg 12.34
def makeAndSignTx(wallet, utxos, pw, etherFeePercent, btc_amount):
    seed = getseed(wallet["encseed"], pw, wallet["ethaddr"])
    balance = sum([o["value"] for o in utxos])
    change = 0
    outputethaddr = wallet["ethaddr"]
    minimum = float(btc_amount) * SATOSHI_PER_BTC + satoshiFee

    if balance == 0:
        raise Exception("No funds in address")
    elif balance < minimum:
        raise Exception("Insufficient funds. Need at least %s BTC (miner fee is 3mBTC)" %
                        str(minimum * 0.00000001))
    else:
        outs = [
            exodus+':'+str(balance - satoshiFee),
            hex_to_b58check(outputethaddr)+':10000'+etherFeePercent.replace('.', ''),
        ]
    tx = mktx(utxos, outs)
    btcpriv = sha3(seed+'\x01')
    for i in range(len(utxos)):
        tx = secure_sign(tx, i, btcpriv)
    return tx


# TODO global minimum removed
def list_purchases(addr):
    if network == TESTNET:
        outs = blockr_unspent(hex_to_b58check(addr, magicbyte), network)
    else:
        outs = unspent(hex_to_b58check(addr))
    txs = {}
    for o in outs:
        if o['output'][65:] == '1':
            h = o['output'][:64]
            try:
                txs[h] = fetchtx(h)
            except:
                txs[h] = blockr_fetchtx(h, network)
    o = []
    for h in txs:
        txhex = txs[h]
        txhex = txhex.encode('ascii')
        txouts = deserialize(txhex)['outs']
        if len(txouts) >= 2 and txouts[0]['value'] >= minimum - satoshiFee:
            addr = script_to_address(txouts[0]['script'], magicbyte)
            if addr == exodus:
                v = txouts[0]['value'] + satoshiFee
                o.append({"tx": h, "value": v})
    return o


def ask_for_password(twice=False):
    if options.pw:
        return pbkdf2(options.pw)
    pw = getpass.getpass()
    if twice:
        pw2 = getpass.getpass()
        if pw != pw2:
            raise Exception("Passwords do not match")
    return pbkdf2(pw)


def ask_for_seed():
    if options.seed:
        return options.seed
    else:
        # uses pybitcointools' 3-source random generator
        return random_key()


def checkwrite(f, thunk):
    exit = False
    try:
        open(f)
        # File already exists
        if not options.overwrite:
            s = "File %s already exists. Overwrite? (y/n) "
            are_you_sure = raw_input(s % f)
            if are_you_sure not in ['y', 'yes']:
                exit = True
    except:
        # File does not already exist, we're fine
        pass
    if exit:
        sys.exit()
    else:
        open(f, 'w').write(thunk())


w = tryopen(options.wallet)
# Generate new wallet
if not len(args):
    args.append('help')
if args[0] == 'genwallet':
    pw = ask_for_password(True)
    newwal = genwallet(ask_for_seed(), pw)
    checkwrite(options.wallet, lambda: json.dumps(newwal))
    print("Your intermediate Bitcoin address is: %s" % newwal['btcaddr'])
    print(" ")
    print("Be absolutely sure to keep the wallet safe and backed up, and do not lose your password")
# Get wallet Bitcoin address
elif args[0] == 'getbtcaddress':
    if not w:
        print("Must specify wallet with -w")
    print(w["btcaddr"])
# Get wallet Ethereum address
elif args[0] == 'getethaddress':
    if not w:
        print("Must specify wallet with -w")
    print(w["ethaddr"])
# Get wallet Bitcoin privkey
elif args[0] == 'getbtcprivkey':
    pw = ask_for_password()
    print(encode_privkey(sha3(getseed(w['encseed'], pw,
                         w['ethaddr'])+'\x01'), 'wif'))
# Get wallet seed
elif args[0] == 'getseed':
    pw = ask_for_password()
    print(getseed(w['encseed'], pw, w['ethaddr']))
# Get wallet Ethereum privkey
elif args[0] == 'getethprivkey':
    pw = ask_for_password()
    print(encode_privkey(sha3(getseed(w['encseed'], pw, w['ethaddr'])), 'hex'))
# Recover wallet seed
elif args[0] == 'recover':
    if not w:
        print("Must have wallet file")
    else:
        pw = ask_for_password()
        print("Your seed is: %s" % getseed(w['encseed'], pw, w['ethaddr']))
# Create the raw transaction for reserving and claiming an ether ticket
elif args[0] == 'makeAndSignTx':
    if len(args) < 3:
        raise Exception("Arguments needed <etherFeePercent> <bitcoinAmount>")
    if not re.match('\d\d\.\d\d', args[1]):
        raise Exception("Ether fee percentage format is xx.xx, example 09.80 for 9.8%")
    try:
        btc_amount = float(args[2])
    except ValueError, e:
        raise Exception("<bitcoinAmount> must be numeric")
    if not w:
        raise Exception("Must specify valid wallet file!")
    try:
        u = unspent(w["btcaddr"])
    except:
        try:
            u = blockr_unspent(w["btcaddr"], network)
        except:
            raise Exception("Blockchain.info and Blockr.io both down. Cannot get transaction outputs to makeAndSignTx. Remember that your funds stored in the intermediate address can always be recovered by running 'python btcToEther.py getbtcprivkey' and importing the output into a Bitcoin wallet like blockchain.info")
    pw = ask_for_password()
    confirm = raw_input("Do you want to makeAndSignTx? (y/n): ")
    if confirm.strip() not in ['y', 'yes', 'Y', 'YES']:
        print("Aborting as you requested")
        sys.exit()

    tx = makeAndSignTx(w, u, pw, args[1], args[2])

    # print("Pushing: %s" % tx)
    # try:
    #     if network == TESTNET:
    #         blockr_pushtx(tx, network)
    #     else:
    #         print(pushtx(tx))
    # except:
    #     try:
    #         print(eligius_pushtx(tx))
    #     except:
    #         raise Exception("Blockchain.info and Eligius both down. Cannot send transaction. Remember that your funds stored in the intermediate address can always be recovered by running 'python btcToEther.py getbtcprivkey' and importing the output into a Bitcoin wallet like blockchain.info")
    print("Here is the Raw Transaction for reserving the ether ticket:\n%s" % tx)
    print("\nWhen the ticket is reserved, the tx hash will be: %s" % txhash(tx))
    print("\nHuman readable tx:\n%s" % deserialize(tx))


elif args[0] == "list":
    if len(args) >= 2:
        addr = args[1]
    elif w:
        addr = w["ethaddr"]
    else:
        raise Exception("Need to specify an address or wallet")
    out = list_purchases(addr)
    if len(out) == 0:
        print("No purchases found.  (You may need to wait for some bitcoin confirmations.)")
    for o in out:
        print("Tx: %s" % o["tx"])
# sha3 calculator
elif args[0] == 'sha3':
    print(sha3(sys.argv[2]).encode('hex'))
# Help
else:
    print('Use "python btcToEther.py genwallet" to generate a wallet')
    print('Use "python btcToEther.py getbtcaddress" to output the intermediate Bitcoin address you need to send funds to')
    print('Use "python btcToEther.py getbtcprivkey" to output the private key to your intermediate Bitcoin address')
    print('Use "python btcToEther.py getethaddress" to output the Ethereum address')
    print('Use "python btcToEther.py getethprivkey" to output the Ethereum private key')
    print('Use "python btcToEther.py makeAndSignTx <etherFeePercent> <bitcoinAmount>" to create the raw transaction once you have deposited to the intermediate address')
    print('Use "python btcToEther.py list" to list purchases made with your wallet')
    print('Use "python btcToEther.py list <ether address>" to list purchases made into that address')
    print('Use -s to specify a seed, -w to specify a wallet file and -p to specify a password when creating a wallet. The -w, -b and -p options also work with other commands.')
