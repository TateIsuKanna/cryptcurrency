import hashlib
import OpenSSL

with open("private.pem", "rb") as key_file:
    private_key=OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM,key_file.read())

class Transaction():
    def __init__(self,sender,recipient,amount):
        self.sender=sender
        self.recipient=recipient
        self.amount=amount
        self.signature=OpenSSL.crypto.sign(private_key,"from"+str(self.sender)+" to"+str(self.recipient)+" "+str(self.amount),"sha256")
    def __str__(self):
        return str(self.sender)+" -> "+str(self.recipient)+" "+str(self.amount)+" "+str(self.signature)[:20]+"..."

class Block():
    def __init__(self):
        self.transactions=[]
        self.proof=b""
        self.previous_hash=b""
    def add_transaction(self,transaction):
        self.transactions.append(transaction)
    def calc_hash(self):
        return hashlib.sha256((str(self.transactions)+str(self.proof)+str(self.previous_hash)).encode()).hexdigest()
    def __str__(self):
        return "previous_hash:"+str(self.previous_hash)+"\n"+"proof:"+str(self.proof)+"\n"+str("\n".join([str(t) for t in self.transactions]))

class Blockchain():
    def __init__(self):
        self.blocks=[]

    def add_block(self,block):
        if len(self.blocks)>0:
            block.previous_hash=self.blocks[-1].calc_hash()
        self.blocks.append(block)
        self.work()

    def work(self):
        while True:
            temp=self.blocks[-1].calc_hash()
            if temp.startswith("0000"):
                print(temp)
                break
            self.blocks[-1].proof=temp

    def __str__(self):
        return str("\n\n".join([str(t) for t in self.blocks]))

ledger=Blockchain()
b=Block()
b.add_transaction(Transaction(0,0xc248712dff34,5000000000000000))
ledger.add_block(b)
print(b)

print()

b=Block()
b.add_transaction(Transaction(0,0x34fff234324,50))
b.add_transaction(Transaction(0xc248712dff34,0x34fff234324,5000000000000000))
b.add_transaction(Transaction(0x34124,0x38748,10))
ledger.add_block(b)
print(b)
