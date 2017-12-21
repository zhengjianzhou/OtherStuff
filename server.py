import json
import requests
from time import time
from urlparse import urlparse
from uuid import uuid4
from flask import Flask, jsonify, request
from block_chain.core_utils import hash, proof_of_work
from block_chain.blockchain import BlockChain
from block_chain.transaction import Transaction
from blockchain.model import Model


def validator(**kwargs):
    return True

model = Model(transation_type=type(Transaction), model_validator=validator)

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
block_chain = BlockChain(model)


@app.route('/mine', methods=['GET'])
def mine():
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = proof_of_work(last_proof)

    txn = Transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    block_chain.add_transactions([txn])
    
    previous_hash = hash(last_block)
    block = block_chain.new_block(proof, previous_hash)

    response = {
        'message'       : "New block mined",
        'index'         : block['index'],
        'transactions'  : block['transactions'],
        'proof'         : block['proof'],
        'previous_hash' : block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    txn = Transaction(**values)
    index = block_chain.add_transactions([txn])
    
    response = {'message': 'Transaction will be added to block {0}'.format(index)}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain'     : block_chain.chain,
        'length'    : len(block_chain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        block_chain.register_node(node)

    response = {
        'message'       : 'New nodes have been added',
        'all_nodes'     : list(block_chain.nodes),
    }
    return jsonify(response), 201


# @app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = block_chain.resolve_conflicts()

    if replaced:
        response = {
            'message'   : 'This chain was replaced',
            'new_chain' : block_chain.chain
        }
    else:
        response = {
            'message'   : 'This chain is authoritative',
            'chain'     : block_chain.chain
        }

    return jsonify(response), 200

# TODO: need a process to call consensus

# APP thread
app.run(host='127.0.0.1', port=5001, threaded=True)
