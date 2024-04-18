import hashlib

def hash_md5(str2hash):
    result = hashlib.md5(str2hash.encode())
    return result.hexdigest()