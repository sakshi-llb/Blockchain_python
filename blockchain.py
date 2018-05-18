import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from urllib.parse import urlparse


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.nodes = []

        # Genesis Block
        self.new_block(previous_hash='1', proof=100)

    def fill_block(self):
        if len(self.pending_transactions) < 4:
            return self.pending_transactions
        else:
            transactions = []
            for index in range(4):
                transactions.append(self.pending_transactions.pop())
            return transactions

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previuos_hash': previous_hash,
            'transactions': []
        }
        block['transactions'] = self.fill_block()
        return block

    def add_block(self, block):
        self.chain.append(block)

    def new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    # @staticmethod
    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.hash_check(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def hash_check(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):

        pass

    def valid_chain(self, chain):

        pass

    def resolve_conflicts(self):
        pass
