import random as rnd

class IDEA:
    def __init__(self, key):
        self.key = self.key_schedule(key)
    
    def key_schedule(self, key):
        # Generate subkeys from the main key
        subkeys = [int.from_bytes(key[i:i+2], 'big') for i in range(0, len(key), 2)]
        return subkeys

    def encrypt_block(self, block):
        # Simplified encryption process for a single block
        # Apply subkeys to the block (placeholder implementation)
        encrypted_block = block
        for subkey in self.key:
            encrypted_block ^= subkey
        return encrypted_block

    def decrypt_block(self, block):
        # Simplified decryption process for a single block
        # Apply subkeys to the block in reverse order (placeholder implementation)
        decrypted_block = block
        for subkey in reversed(self.key):
            decrypted_block ^= subkey
        return decrypted_block

    def encrypt(self, plaintext, iv):
        # Encrypt plaintext in CFB mode
        ciphertext = bytearray()
        prev_cipher = iv
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            encrypted_block = self.encrypt_block(int.from_bytes(prev_cipher, 'big'))
            cipher_block = int.from_bytes(block, 'big') ^ encrypted_block
            ciphertext.extend(cipher_block.to_bytes(8, 'big'))
            prev_cipher = cipher_block.to_bytes(8, 'big')
        return bytes(ciphertext)

    def decrypt(self, ciphertext, iv):
        # Decrypt ciphertext in CFB mode
        plaintext = bytearray()
        prev_cipher = iv
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            encrypted_block = self.encrypt_block(int.from_bytes(prev_cipher, 'big'))
            plain_block = int.from_bytes(block, 'big') ^ encrypted_block
            plaintext.extend(plain_block.to_bytes(8, 'big'))
            prev_cipher = block
        return bytes(plaintext)

