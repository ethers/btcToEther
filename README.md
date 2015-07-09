### DON'T LOSE YOUR WALLET OR YOUR PASSWORD

#### Instructions for ether `Buyer`:

1. First, go to EthereumBitcoinSwap and choose which ether ticket you want to get.  Note the ticket ID, `Bitcoin address` and the total price `bitcoinAmount`.
1. `python btcToEther.py genwallet`, enter a password
1. Make sure you write down the password or otherwise keep it safe, and make sure you backup your wallet file (saved at btcToEtherWallet.json by default, you can use -w to save it somewhere else)
1. Send the `bitcoinAmount` + 0.0003BTC (miner fee) into the intermediate address (`python btcToEther.py getbtcaddress`).  If you change your mind, you can still
get the bitcoins in the intermediate address.  The miner fee helps ensure that
your Bitcoin payment to the ether seller will be mined in a timely manner.
1. If you do not have any ethers already, decide an `etherFeePercent` for the
3rd party that will submit (2) Ethereum transactions for you.  Important: you
may specify `etherFeePercent` of zero, but take a big risk that the required
Ethereum transactions will not be performed for you.
1. Use `python btcToEther.py makeAndSignTx <etherFeePercent> <bitcoinAmount> <Bitcoin address>` to create a raw Bitcoin transaction and hash.  Do not broadcast this
Bitcoin transaction.  A few steps later, you will give the hash only, to a 3rd
party.
1. Go back to EthereumBitcoinSwap, click Help, and then enter your Bitcoin
transaction hash and ticket ID.  Click Compute.  It will take a random amount
of minutes to compute a proof of work nonce: be patient and multitask (it is
a small inconvenience for a trustless, secure exchange).
1. When a nonce has been computed, give the nonce, Bitcoin transaction hash
(only the hash) and the ticket ID, to a 3rd party that has ethers:
make sure `etherFeePercent` is non-zero so that a 3rd party will help you.
If you already have ethers, you can avoid a 3rd party and be a `Claimer` yourself following the `Claimer` instructions.
1. Coordinate with 3rd party for them to reserve the ticket (they follow `Claimer`
instructions below)
1. Go back to EthereumBitcoinSwap and check that your ticket has been reserved
by the 3rd party.
1. Once the ticket has been reserved, time is ticking and as soon as you can,
broadcast your Bitcoin transaction (by using the tool of your choice, eg https://blockchain.info/pushtx)
Once broadcasted you will no longer be able to change your mind and get your
bitcoins back.
1. Wait until the Bitcoin transaction has 6 confirmations and then request the
3rd party to claim your ticket.
1. If 2 hours have elapsed since the 3rd party reserved the ticket, you may
seek the assistance of anyone else who has ethers, to claim the ticket for you.
Again, the `etherFeePercent` above is important so that someone will want to help
you.  This step must be completed within another 2 hours: tickets are only
reserved for a total of 4 hours, and afterwards you need to reserve it again,
or someone else can reserve the ticket and use their own bitcoins to claim
the ethers (your bitcoins will already have been sent to the ether seller).

#### `Claimer` instructions:

1. On EthereumBitcoinSwap, look for the ticket using the ID, and click Reserve.
1. Enter the Bitcoin transaction hash, Proof of Work (nonce provided by `Buyer`)
1. You should now be able to click the Reserve button.  Click it.
1. Assuming the Proof of Work is valid, wait for the Ethereum transaction to
reserve the ticket.
1. When the ticket is reserved, monitor and wait until the Bitcoin transaction
has 6 confirmations.
1. Go back to EthereumBitcoinSwap, look for the ticket using the ID, and click
Claim.
1. You should now be able to click the Claim button.  Click it.


#### Result of swap:

* `Claimer` will get `etherFeePercent` of the number of ethers in the ticket.

* `Buyer` will have the number of ethers in the ticket, less the fee paid to the Claimer.

* `Seller` has the bitcoins they desired at the Bitcoin address they specified
in the ticket.


#### Future

Servers can be setup as the 3rd party.  A server can listen for buyers to
provide it with a ticket ID, Bitcoin transaction hash, and proof of work.
A server can quickly check the validity (without expending any ethers) before
reserving the ticket. Servers will monitor the Bitcoin blockchain, as well as
the ether tickets that are claimable, and automatically claim tickets. The
incentive for servers to provide this service is automated collection of ether
fees from buyers, and servers do not need to post any collateral.

EthereumBitcoinSwap can be extended to list such servers, and a buyer could
choose which server to use.  EthereumBitcoinSwap could also make it easier
for buyers and choose servers automatically, as well as notify all servers
about all tickets, so that any unclaimed tickets, can be claimed by any
server when the initial 2 hour period elapses.  This will eliminate the
coordination a buyer would have to do if the 3rd party were a human.  With servers:
a buyer submits a request to reserve a ticket; server reserves immediately;
buyer broadcasts Bitcoin transaction; server immediately claims ticket
when Bitcoin transaction has 6 confirmations.


#### Notes

EthereumBitcoinSwap is at http://TODO


Additional instructions:

* To recover the private key of your BTC intermediate address, use `python btcToEther.py getbtcprivkey`
* To show your BTC intermediate address, use `python btcToEther.py getbtcaddress`
* To recover your ETH privkey, use `python btcToEther.py getethprivkey`
* To show your ETH address, use `python btcToEther.py getethaddress`
* Use `-w /path/to/wallet.json` if you want to point to a specific wallet file or save your wallet at a specific location
