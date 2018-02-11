import hashlib
import OpenSSL
import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

with open("private.pem", "rb") as key_file:
    private_key=serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

class Transaction():
    def __init__(self,sender,recipient,amount):
        self.sender=sender
        self.recipient=recipient
        self.amount=amount
        

        p=datetime.datetime.now()
        self.signature=OpenSSL.crypto.sign(OpenSSL.crypto.PKey.from_cryptography_key(private_key),"from"+str(self.sender)+" to"+str(self.recipient)+" "+str(self.amount),"sha256")
    def __repr__(self):
        return "from"+str(self.sender)+" to"+str(self.recipient)+" "+str(self.amount)+str(self.signature)

class Block():
    def __init__(self):
        self.transactions=[]
        self.proof=b""
        self.previous_hash=b""
    def add_transaction(self,transaction):
        self.transactions.append(transaction)
    def calc_hash(self):
        return hashlib.sha256((str(self.transactions)+str(self.proof)+str(self.previous_hash)).encode()).hexdigest()
    def work(self,ledger=None):
        if ledger:
            self.previous_hash=ledger.blocks[-1].calc_hash()
        while True:
            temp=self.calc_hash()
            if temp.startswith("000"):
                print(temp)
                break
            self.proof=temp

    def __repr__(self):
        return "previous_hash:"+str(self.previous_hash)+"\n"+"proof:"+str(self.proof)+"\n"+str("\n".join([str(t) for t in self.transactions]))

class Blockchain():
    def __init__(self):
        self.blocks=[]

    def add_block(self,block):
        self.blocks.append(block)

    def __repr__(self):
        return str("\n\n".join([str(t) for t in self.blocks]))

    #@staticmethod
    #def hash(block):
    #    pass

    #@property
    #def last_block(self):
    #    pass

ledger=Blockchain()
b=Block()
b.add_transaction(Transaction(0,0xc248712dff34,5000000000000000))
b.work()
ledger.add_block(b)

b=Block()
b.add_transaction(Transaction(0,0x34fff234324,50))
b.add_transaction(Transaction(0xc248712dff34,0x34fff234324,5000000000000000))
b.add_transaction(Transaction(0x34124,0x38748,10))
b.work(ledger)
ledger.add_block(b)

import random
for i in range(100):
    b=Block()
    for j in range(random.randint(1,10)):
        b.add_transaction(Transaction(random.randint(0,10000000),random.randint(0,10000000),random.randint(0,38491834341)))
    b.work(ledger)
    print(b)
    ledger.add_block(b)
