 #! /usr/bin/python3
import datetime
import json
import hashlib

class Blockchain: 

    def __init__(self):
        self.__chain = []
        self.__transaction = 0 
        # genesis block
        self.createBlock(1,'0'*64)

    def addTransaction(self):
        self.__transaction += 1

    def getTransaction(self):
        return self.__transaction

    def getChain(self):
        return self.__chain

    def getPrevBlock(self):
        return self.__chain[-1]

    def createBlock(self,nonce,prev_hash):
        block = {
            'index' : len(self.__chain) + 1,
            'timestamp' : str(datetime.datetime.now()),
            'nonce' : nonce,
            'data': self.__transaction,
            'prev_hash' : prev_hash
        }
        self.__chain.append(block)
        return block

    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        encoded_block = hashlib.sha256(encoded_block).hexdigest()
        return encoded_block
    
    # difficulty -> '0000x'
    def proofOfWork(self,prev_nonce):
        new_nonce = 1
        check_proof = False
        #puzzle
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_nonce**2 - prev_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    def isChainValid(self,chain):
        prev_block = chain[0]
        block_index = 1
        while block_index != len(chain):

            block =  chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False

            prev_nonce = prev_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - prev_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            prev_block = block
            block_index +=1
        return True

blockchain = Blockchain()