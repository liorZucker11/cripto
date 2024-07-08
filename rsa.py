import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def generate_rsa_keys(bits=2048):
    p = random.getrandbits(bits // 2)
    q = random.getrandbits(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    return (e, n), (d, n)

def rsa_encrypt(message, pubkey):
    e, n = pubkey
    cipher = pow(message, e, n)
    return cipher

def rsa_decrypt(cipher, privkey):
    d, n = privkey
    message = pow(cipher, d, n)
    return message
