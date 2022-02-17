from crypt import methods
from urllib import response
from flask import Flask, jsonify
from numpy import block
import blockchain

app = Flask(__name__)

@app.route('/')
def hello():
    return '<p>Server is onlines</p>'

@app.route('/get_chain',methods = ["GET"])
def get_chain():
    response = {
        'chain': blockchain.blockchain.getChain(),
        'length': len(blockchain.blockchain.getChain())
    }

    return jsonify(response),200

@app.route('/mining',methods = ["GET"])
def mining_block():
    blockchain.blockchain.addTransaction()

    prev_block = blockchain.blockchain.getPrevBlock()
    prev_block_nonce = prev_block['nonce']

    new_nonce = blockchain.blockchain.proofOfWork(prev_nonce=prev_block_nonce)

    prev_block_hash = blockchain.blockchain.hash(prev_block)

    new_block = blockchain.blockchain.createBlock(nonce=new_nonce,prev_hash=prev_block_hash)

    response = {
        "message":"block was mined",
        'index' : new_block['index'],
        'nonce': new_block['nonce'],
        'data': blockchain.blockchain.getTransaction(),
        'preious_hash' : new_block['prev_hash']
    }
    return jsonify(response),200

@app.route('/is_chain_valid',methods=['GET'])
def is_chain_valid():
    is_valid = blockchain.blockchain.isChainValid(blockchain.blockchain.getChain())
    if is_valid:
        response = {
            'message' : 'Block is valid'
        }
    else:
        response = {
            'message' : 'Block is invalid'
        }
    return jsonify(response),200
if __name__ == "__main__":
    app.run(debug=True)