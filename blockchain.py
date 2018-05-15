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
        self.current_transactions = []

        self.nodes = set()

        # Genesis Block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        pass

    def new_transaction(self, sender, recipient, amount):
        pass

    # @staticmethod
    def hash(self, block):
        pass

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        pass

    @staticmethod
    def valid_proof(last_proof, proof):
        pass

    def register_node(self, address):

        pass

    def valid_chain(self, chain):

        pass

    def resolve_conflicts(self):
        pass
