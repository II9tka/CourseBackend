import hashlib


def hash_token(token: str) -> str:
    algorithm = hashlib.sha256()
    algorithm.update(token.encode('utf-8'))
    return algorithm.hexdigest()
