from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_password_hash(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hash: str):
    return password_hash.verify(password, hash)