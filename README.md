Notes:

###DON'T LOSE YOUR WALLET OR YOUR PASSWORD

####Instructions for ether `Buyer`:

1. First, go to EthereumBitcoinSwap and choose which ether ticket you want to get.  Note the ticket ID, `Bitcoin address` and the total price `bitcoinAmount`.
1. `python btcToEther.py genwallet`, enter a password
1. Make sure you write down the password or otherwise keep it safe, and make sure you backup your wallet file (saved at btcToEtherWallet.json by default, you can use -w to save it somewhere else)
1. Send the `bitcoinAmount` into the intermediate address provided.  If you
change your mind, you can still get the bitcoins in the intermediate address.
1. If you do not have any ethers already, decide an `etherFeePercent` for the
3rd party that will indirectly send you the ethers in the ticket you chose.
1. Use `python btcToEther.py makeAndSignTx <etherFeePercent> <bitcoinAmount> <Bitcoin address>` to create a raw Bitcoin transaction and hash.  Do not broadcast this
Bitcoin transaction.  A few steps later, you will give the hash only, to a 3rd
party.
1. Go back to EthereumBitcoinSwap, click Help, and then enter your Bitcoin
transaction hash and ticket ID.  Click Compute.  It will take a random amount
of minutes to compute a proof of work: be patient and multitask.
1. When a nonce has been computed, give the nonce, Bitcoin transaction hash
(only the hash) and the ticket ID, to a 3rd party you trust that has ethers:
make sure `etherFeePercent` is non-zero so that a 3rd party will help you.
If you already have ethers, you can avoid a 3rd party and be a `Claimer` yourself following the next instructions.
1. Coordinate with 3rd party for them to reserve the ticket, go back to EthereumBitcoinSwap and check that your ticket has been reserved by the 3rd
party.
1. When the ticket has been reserved, broadcast your Bitcoin transaction (by
using tool of your choice, eg https://blockchain.info/pushtx)
Once broadcasted you will no longer be able to change your mind and cancel
the swap for ethers with bitcoins.
1. Wait until Bitcoin transaction has 6 confirmations and then request the 3rd
party to claim your ticket.
1. If 2 hours have elapsed since the 3rd party reserved the ticket, you may
seek the assistance of anyone else who has ethers, to claim the ticket for you.
Again, the `etherFeePercent` is important so that someone will want to help
you.

####`Claimer` instructions:

1. On EthereumBitcoinSwap, look for the ticket using the ID, and click Reserve.
1. Enter the Bitcoin transaction hash, Proof of Work (provided by `Buyer`)
1. You should now be able to click the Reserve button.  Click it.
1. Assuming the Proof of Work is valid, wait for the Ethereum transaction to
reserve the ticket.
1. When the ticket is reserved, monitor and wait until the Bitcoin transaction
has 6 confirmations.
1. Go back to EthereumBitcoinSwap, look for the ticket using the ID, and click
Claim.
1. You should now be able to click the Claim button.  Click it.


####Result of swap:

* `Claimer` will get `etherFeePercent` of the number of ethers in the ticket.

* `Buyer` will have the number of ethers in the ticket, less the fee paid to the Claimer.

* `Seller` has the bitcoins they desired at the Bitcoin address they specified
in the ticket.


EthereumBitcoinSwap is at http://TODO


Additional instructions:

* To recover the private key of your BTC intermediate address, use `python btcToEther.py getbtcprivkey`
* To show your BTC intermediate address, use `python btcToEther.py getbtcaddress`
* To recover your ETH privkey, use `python btcToEther.py getethprivkey`
* To show your ETH address, use `python btcToEther.py getethaddress`
* Use `-w /path/to/wallet.json` if you want to point to a specific wallet file or save your wallet at a specific location
