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

        self.nodes = set()

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
        self.chain.append(block)

        return block

    def recieve_block(self, block):

        self.chain.append(block)
        return True

    def new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    @staticmethod
    def hash(block):
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

    def register_node(self, address):

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.hash_check(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def replace_chain(self):
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


# from uuid import uuid4

# Blockchain = Blockchain()

# # Blockchain.register_user(uuid4().hex)
# # Blockchain.register_user(1234)
# # print(Blockchain.users)
# block = {
#     'index':  1,
#     'timestamp': time(),
#     'proof': 'proof',
#     'previuos_hash': 'previous_hash',
#     'transactions': []
# }

# block = json.dumps(block)

# block = Blockchain.recieve_block(block)

# print(Blockchain.chain)
