import pprint
import requests
from stellar_base.keypair import Keypair
from stellar_base.utils import StellarMnemonic
from stellar_base.address import Address
from stellar_base.builder import Builder


kp = Keypair.random()
publickey = kp.address().decode()
r = requests.get('https://horizon-testnet.stellar.org/friendbot?addr=' + publickey)


#or

sm = StellarMnemonic() #create mnemonic string (random group of words)
m = sm.generate()
# kp3 = Keypair.deterministic(m) #keypair of public & secret key

# #index not working
kp1 = Keypair.deterministic(m)
# publickey = kp3.address().decode()
# seed = kp3.seed().decode() #your secret key


address = Address(address=publickey)
address.get()

pp = pprint.PrettyPrinter(width=41, compact=True)
print("balances: {}\n".format(address.balances))
print("sequence: {}\n".format(address.sequence))
print("flags: {}\n".format(address.flags))
print("signers: {}\n".format(address.signers))
print("data: {}\n".format(address.data))
# pp.pprint("paymentss: {}\n".format(address.payments()))
# pp.pprint("transactionss: {}\n".format(address.transactions()))
# pp.pprint("effectss: {}\n".format(address.effects()))
# pp.pprint("offerss: {}\n".format(address.offers()))
# pp.pprint("operationss: {}\n".format(address.operations()))


seed = kp.seed().decode()
builder = Builder(secret=seed) #for live network=public

bob_address = "GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG"
builder.append_payment_op(bob_address, '100', 'XLM')

builder.add_text_memo('test 1')

builder.sign()
builder.submit()
