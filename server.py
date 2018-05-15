import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain_self import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    pass


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    pass


@app.route('/chain', methods=['GET'])
def full_chain():
    pass


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    pass


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
