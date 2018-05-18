import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
user_id = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():

    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    miner = "test_server"

    block = blockchain.new_block(proof, last_proof, miner)
    # block['transaction'].append({
    #     'sender': 0,
    #     'recipient': mine_user_id,
    #     'amount': 1
    # })

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to the Block'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = jsonify(blockchain.chain)
    return response, 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    pass


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
