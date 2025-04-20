import hashlib


def hashValue(
    value: str,
    hash_size: int = 10
) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:hash_size]
