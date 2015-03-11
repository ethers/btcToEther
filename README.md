Notes:

DON'T LOSE YOUR WALLET OR YOUR PASSWORD

Instructions:

1. `python btcToEther.py genwallet`, enter a password
2. Make sure you write down the password or otherwise keep it safe, and make sure you backup your wallet file (saved at btcToEtherWallet.json by default, you can use -w to save it somewhere else)
3. Send BTC into the intermediate address provided
4. Use `python btcToEther.py finalize` to send the BTC from the intermediate address to the btcrelay
5. Copy the Transaction Hash and paste it to btcrelay at http://TODO and click on Lookup
6. Wait for at least 6 confirmations and then click Claim Ether

Additional instructions:

* To recover the private key of your BTC intermediate address, use `python btcToEther.py getbtcprivkey`
* To show your BTC intermediate address, use `python btcToEther.py getbtcaddress`
* To recover your ETH privkey, use `python btcToEther.py getethprivkey`
* To show your ETH address, use `python btcToEther.py getethaddress`
* Use `-w /path/to/wallet.json` if you want to point to a specific wallet file or save your wallet at a specific location
