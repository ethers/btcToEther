Notes:

DON'T LOSE YOUR WALLET OR YOUR PASSWORD

Instructions for ether `Buyer`:

1. First, go to EthereumBitcoinSwap and choose which ether ticket you want to get.  Note the ticket ID, `Bitcoin address` and the total price `bitcoinAmount`.
1. `python btcToEther.py genwallet`, enter a password
1. Make sure you write down the password or otherwise keep it safe, and make sure you backup your wallet file (saved at btcToEtherWallet.json by default, you can use -w to save it somewhere else)
1. Send the `bitcoinAmount` into the intermediate address provided.  If you
change your mind, you can still get the bitcoins in the intermediate address.
1. If you do not have any ethers already, decide an `etherFeePercent` for the
third party that will indirectly send you the ethers in the ticket you chose.
1. Use `python btcToEther.py makeAndSignTx <etherFeePercent> <bitcoinAmount> <Bitcoin address>` to create a raw Bitcoin transaction.  Do not broadcast this
transaction.  Give this transaction and the ticket ID, to a third party you trust that has ethers.  If you already have ethers, you can avoid a third
party and be a `Claimer` yourself following the next instructions.


`Claimer` instructions:
1. On EthereumBitcoinSwap, look for the ticket using the ID.
1. Enter the raw Bitcoin transaction and click Lookup.
1. You should now be able to click the Reserve button.  Click it.
1. Follow the instruction to broadcast the raw Bitcoin transaction.
1. Monitor and wait until the transaction has 6 confirmations.
1. On EthereumBitcoinSwap, look for the ticket using the ID.
1. You should now be able to click the Claim button.  Click it.


The result of the swap will be:

* `Claimer` will have their ether security deposit returned 100%, plus `etherFeePercent` of the number of ethers in the ticket.

* `Buyer` will have the number of ethers in the ticket, less the fee paid to the Claimer.

* `Seller` has the bitcoins they desired at the Bitcoin address they specified in the ticket.


EthereumBitcoinSwap is at http://TODO


Additional instructions:

* To recover the private key of your BTC intermediate address, use `python btcToEther.py getbtcprivkey`
* To show your BTC intermediate address, use `python btcToEther.py getbtcaddress`
* To recover your ETH privkey, use `python btcToEther.py getethprivkey`
* To show your ETH address, use `python btcToEther.py getethaddress`
* Use `-w /path/to/wallet.json` if you want to point to a specific wallet file or save your wallet at a specific location
