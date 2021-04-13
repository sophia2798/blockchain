# IMPORT MODULES
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request

# CREATE BLOCKCHAIN CLASS
class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # CREATE GENESIS BLOCK
        self.new_block(previous_hash=1, proof=100)

    # NEW BLOCK METHOD (create new block and add to the chain)
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # reset current transactions list
        self.current_transactions = []
        self.chain.append(block)

        return block

    # NEW TRANSACTION METHOD (create new transaction for next mined block)
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    # PROPERTY DECORATOR TO RETURN THE LAST BLOCK
    @property
    def last_block(self):
        return self.chain[-1]

    # HASH METHOD (create SHA-256 hash of a block)
    # TURN HASH METHOD INTO STATIC METHOD (cannot modify class or object)
    @staticmethod
    def hash(block):
        # must have an ORDERED dictionary
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    # PROOF OF WORK (POW) METHOD (where check condition is hash(pp') has 4 leading 0s)
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    # TURN VALID PROOF METHOD INTO STATIC METHOD (validates if hash has 4 leading 0s)
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == '0000'

'''
CODE BELOW IS FOR SETTING UP API TO MAKE HTTP REQUESTS TO THE BLOCKCHAIN
'''

# INSTANTIATE NODE
app = Flask(__name__)

# GENERATE GLOBALLY UNIQUE ADDRESS FOR NODE
node_id = str(uuid4()).replace('-','')

# INSTANTIATE BLOCKCHAIN
blockchain = Blockchain()

# CREATE ROUTES
@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
