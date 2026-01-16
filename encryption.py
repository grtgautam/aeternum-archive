from cryptography.fernet import Fernet

def generate_key():
    """Generates a key for encryption."""
    return Fernet.generate_key()

def encrypt_data(data: bytes, key: bytes) -> bytes:
    """Encrypts bytes data using the provided key."""
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypts bytes data using the provided key."""
    f = Fernet(key)
    return f.decrypt(encrypted_data)
