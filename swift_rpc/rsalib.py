#coding:utf-8
import rsa

def create_key():
    (pubkey, privkey) = rsa.newkeys(1024)
    pub = pubkey.save_pkcs1()
    pubfile = open('public.pem','w+')
    pubfile.write(pub)
    pubfile.close()
    
    pri = privkey.save_pkcs1()
    prifile = open('private.pem','w+')
    prifile.write(pri)
    prifile.close()

def load_public():
    with open('public.pem') as publickfile:
        p = publickfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)
    return pubkey
    
def load_private():
    with open('private.pem') as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)
    return privkey

def encrypt(message):
    crypto = rsa.encrypt(message, pubkey)
    return crypto

def decrypt(crypto):
    message = rsa.decrypt(crypto, privkey)
    return message

pubkey = load_public()
privkey =  load_private()

if __name__ == "__main__":
    message = 'hello' 
    en_str = encrypt(message)
    print en_str
    print decrypt(en_str)
