from Cryptodome.Util.number import getPrime, bytes_to_long, long_to_bytes  # , inverse
import random


def generate_keys(bits=256):
    p = getPrime(bits)
    g = random.randint(2, p - 2)
    x = random.randint(1, p - 2)  # Private key
    y = pow(g, x, p)  # Public key (y = g^x mod p)
    return (p, g, y), x  # (public_key, private_key)


def encrypt(public_key, plaintext):
    p, g, y = public_key
    k = random.randint(1, p - 2)
    a = pow(g, k, p)
    b = (pow(y, k, p) * bytes_to_long(plaintext)) % p
    return a, b


def decrypt(private_key, public_key, ciphertext):
    a, b = ciphertext
    p, g, y = public_key
    x = private_key
    # s = pow(a, x, p)
    # # plaintext = (b * inverse(s, p)) % p
    # plaintext = (b * pow(s, -1, p)) % p
    plaintext = b * pow(a, -x, p) % p
    return long_to_bytes(plaintext)


public_key, private_key = generate_keys()
print("Keys:", public_key, private_key)
plaintext = b"Hello, ElGamal!"
ciphertext = encrypt(public_key, plaintext)
decrypted_plaintext = decrypt(private_key, public_key, ciphertext)

print("Original:", plaintext)
print("Encrypted:", ciphertext)
print("Decrypted:", decrypted_plaintext)
