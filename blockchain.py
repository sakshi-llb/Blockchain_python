import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.users = set()

        # Genesis Block
        self.new_block(proof=100, previous_hash=1, miner='genesis')

    def fill_block(self):
        if len(self.pending_transactions) < 4:
            transactions = []
            transactions = self.pending_transactions
            self.pending_transactions = []
            return transactions

        else:
            transactions = []
            for index in range(4):
                transactions.append(self.pending_transactions.pop(-index))
            return transactions

    def new_block(self, proof, previous_hash, miner):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previuos_hash': previous_hash,
            'transactions': self.fill_block()
        }
        if miner != 'genesis':
            block['transactions'].append({
                'sender': 0,
                'recipient': miner,
                'amount': 1
            })
        self.chain.append(block)
        self.share_new_blocks(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    @staticmethod
    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_hash):
        proof = 0
        while self.hash_check(previous_hash, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def hash_check(previous_hash, proof):
        guess = f'{previous_hash}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_user(self, users):
        self.users.add(users)

    def share_new_blocks(self, block):
        for user in self.users:
            url = f'localhost://{user}/shared_block'
            requests.post(url, data=json.dumps(block))

    def add_shared_blocks(self, block):
        self.chain.append(block)

    def valid_chain(self, chain):

        pass

    def resolve_conflicts(self):
        pass


# from uuid import uuid4

# Blockchain = Blockchain()

# Blockchain.register_user(uuid4().hex)
# Blockchain.register_user(1234)
# print(Blockchain.users)
