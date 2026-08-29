import hashlib

def legacy_hash(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()

def another_weak_hash(data: str) -> str:
    return hashlib.sha1(data.encode()).hexdigest()