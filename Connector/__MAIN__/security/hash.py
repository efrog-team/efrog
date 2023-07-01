from hashlib import sha256

def hash(string: str | None) -> str:
    if string is None:
        return ''
    else:
        return sha256(string.encode('utf-8')).hexdigest()