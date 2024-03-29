import hashlib
import OpenSSL
import base64
import cryptography
import struct

class CryptcurrencyUtil():
    @classmethod
    def publickey_to_address(self,pub):
        digest=hashlib.sha256(pub).digest()
        return base64.b64encode(digest+hashlib.sha256(digest).digest()[:4]).decode()

class Transaction():
    def __init__(self,sender,recipient,amount):
        #TODO:不正なアドレス
        self.sender=sender
        self.recipient=recipient
        self.amount=amount
        self.signature=b""
    def sign(self,private_key):
        self.signature=OpenSSL.crypto.sign(private_key,struct.pack("<294s294sQ",self.sender,self.recipient,self.amount),"sha256")

    def __str__(self):
        return base64.b64encode(self.sender).decode()[:30]+"... -> "+base64.b64encode(self.recipient).decode()[:30]+"... "+str(self.amount)+" "+str(self.signature)[:30]+"..."

class Block():
    def __init__(self):
        self.previous_hash=b""
        self.transactions=[]
        self.nonce=b""
    def add_transaction(self,transaction):
        #TODO:署名確認
        #TODO:残高確認
        self.transactions.append(transaction)
    def calc_hash(self):
        return hashlib.sha256((str(self.previous_hash)+str(self.transactions)+str(self.nonce)).encode()).hexdigest()
    def __str__(self):
        return "previous_hash "+str(self.previous_hash)+"\n"+"nonce "+str(self.nonce)+"\n"+str("\n".join([str(t) for t in self.transactions]))

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
            temp_nonce=self.blocks[-1].calc_hash()
            if temp_nonce.startswith("0000"):
                print(temp_nonce)
                break
            self.blocks[-1].nonce=temp_nonce

    def __str__(self):
        return str("\n\n".join([str(t) for t in self.blocks]))

ledger=Blockchain()

with open("private.pem", "rb") as key_file:
    private_key=OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM,key_file.read())
s=private_key.to_cryptography_key().public_key().public_bytes(cryptography.hazmat.primitives.serialization.Encoding.DER,cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo)
m=base64.b64decode("MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2zSJb6e9tJKfKSNKDOWL zxa/9ZOfquIXuZA/4QGvuvasT7km8IamyTS3Ft0jXjCaGstiFy2jKcLv6rumiC4A bkkwPGpBT0bnhpDfnGXRlL2qvK4sgZkNc/3DFjbbIFzZy3TaCt41+KpRY7aP9Epp C+kVB9YQ+lg5CcUAqFL2i2i9PbonE/3W5p5f0C/ewiiPWfEoSD6zDP2ZRKPMpVbF NQL2iw1LnYeZKEp9SWwA+h/VTt3p0do1Z5hfNe6WdbrdHsl9cBzP5KjfecqqORSZ gZAF13ubLtsNEsJXop375CcJ4O8n0ub0KJaPZVKdiqayrDd1gC+CXekKNxYZfMDp yQIDAQAB")

print(CryptcurrencyUtil.publickey_to_address(m))

t=Transaction(s,m,5000000000000000)
t.sign(private_key)

b=Block()
b.add_transaction(t)
ledger.add_block(b)

print(ledger)
