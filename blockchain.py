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
    def new_block(self, proof, previous_hash):
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