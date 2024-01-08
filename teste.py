import secrets

# Gere uma chave de 32 bytes (256 bits) para maior segurança
secret_key = secrets.token_hex(32)

print(secret_key)