import hashlib
import json
from time import time

from flask import Flask, jsonify, request
from argparse import ArgumentParser
parser = ArgumentParser()

from blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)


# Instantiate the Blockchain
blockchain = Blockchain()

miner = 'test'  # solve the miner problem XD


@app.route('/mine', methods=['GET'])
def mine():

    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    block = blockchain.new_block(proof, last_proof, miner)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof']
    }
    return jsonify(response), 200


# @app.route('/shared_block', methods=['POST'])
# def add_block():
#     block = request.get_json()
#     blockchain.add_shared_blocks(block)
#     return


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Create a new Transaction
    blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'])

    response = {'message': 'Transaction will be added to the Block'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = jsonify(blockchain.chain)
    return response, 200


# @app.route('/init', methods=['POST'])
# def register_user():
#     val = request.get_json()
#     blockchain.register_user(val)
#     response = {
#         'Message': f'Node Joined',
#         'User Count': len(blockchain.users)
#     }
#     return jsonify(response), 200


@app.route('/consensus', methods=['GET'])
def consensus():
    pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)
