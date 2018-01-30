#run teenee_blockchain.py
#type in a number of blockchain to be created

from datetime import datetime #only getting the datetime class from datetime library
import hashlib as hasher

class Block: #create block class with following arguments
	def __init__(self, index, timestamp, data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.hash_block()

	def __str__(self): #when called, it creates a string with the index e.g Block#1
		return 'Block#{}'.format(self.index)

	def hash_block(self):
		sha = hasher.sha256() #function for hashing input in SHA256
		seq = (str(x) for x in (self.index, self.timestamp, self.data, self.previous_hash))
		#string of the arguments
		sha.update(''.join(seq).encode('utf-8'))#update hash, squishes into one sentence and return an encoded version in utf 8
		return sha.hexdigest()#returned as a string of double lenght, contain only hexadecimal digits()

def make_genesis_block(): #the big bang for blockchain
	block = Block(index=0, timestamp=datetime.now(), data="Genesis Block", previous_hash="0")
	return block

def next_block(last_block, data=''):
	idx = last_block.index + 1
	block = Block(index=idx, timestamp=datetime.now(), data='{}{}'.format(data, idx), previous_hash=last_block.hash)
	return block

def test_code(num):
	blockchain = [make_genesis_block()] #start with the genesis block
	prev_block = blockchain[0]
	for num in range(0, num):
		block = next_block(prev_block, data='some data here')
		blockchain.append(block) #prev hash and block produced, pushed at the back of the list
		prev_block = block
		print('{} added to blockchain'.format(block))
		print('Hash: {}\n'.format(block.hash))

def start_mining(): #input for user to type amt of blocks created, catch for non-integers added
	lenght_of_block = input('How many blocks do you want produce?\n')
	if lenght_of_block.isdigit() :
		test_code(int(lenght_of_block))
	else:
		print('Not a number, type a number!')
		start_mining()

#run code
start_mining()