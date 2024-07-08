import rsa , idea , ElgamalEllipticCurve , random as rnd
# IDEA encryption/decryption

def createIv():
    iv = ""
    for i in range(8):
        number = rnd.randint(97, 122)
        iv += chr(number)
    return iv
    
def createKey():
    key=''
    for i in range (16):
        key+=str(rnd.randint(0,9))
    return key

iv = createIv().encode() 
key = createKey().encode()
plaintext = b'Hello!'
idea = idea.IDEA(key)
ciphertext = idea.encrypt(plaintext, iv)
decrypted_text = idea.decrypt(ciphertext, iv)

# RSA encryption/decryption of the IDEA key
pubkey, privkey = rsa.generate_rsa_keys()
encrypted_key = rsa.rsa_encrypt(int.from_bytes(key, 'big'), pubkey)
decrypted_key = rsa.rsa_decrypt(encrypted_key, privkey).to_bytes(256, 'big')

# EC El-Gamal signing and verification
curve = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
ec_privkey, ec_pubkey = ElgamalEllipticCurve.generate_ec_keys()
signature = ElgamalEllipticCurve.ec_sign(ciphertext, ec_privkey, curve)
is_valid = ElgamalEllipticCurve.ec_verify(ciphertext, signature, ec_pubkey, curve)

print(f'Ciphertext: {ciphertext}')
print(f'Decrypted text: {decrypted_text}')
print(f'Encrypted IDEA key: {encrypted_key}')
print(f'Decrypted IDEA key: {decrypted_key}')
print(f'Signature: {signature}')
print(f'Signature valid: {is_valid}')
