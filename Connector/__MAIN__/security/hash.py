from hashlib import sha256

def hash(string):
    return sha256(string.encode('utf-8')).hexdigest()