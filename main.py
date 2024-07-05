# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 09:06:58 2024

@author: Leen
"""
import lea
import OFB
import ElgamalEllipticCurve as gm
import rsa
import sys

def get_ascii_values(string):
    ascii_values = [ord(char) for char in string]
    padded_values = ''.join([str(value).zfill(3) for value in ascii_values])
    return padded_values

def get_characters_from_ascii_values(b):
    try:
        if (len(b)%3)!=0:
            b=b.zfill(len(b)+len(b)%3-1)
        ascii_values = [(int(b[i:i+3])) for i in range(0, len((b)), 3)]
        characters = ''.join([chr(value) for value in ascii_values])
        return characters
    except ValueError:
        print("Invalid input format.")
        

def main():
    
   print('Alice wants to send an Email to Bob')
   print('-------------------------------------')
   print('Generating symmetric key to encrypt email using LEA, OFB mode')
   print('-------------------------------------')
   
   # Generate keys
   k = "1" + lea.get_random_bits(127) # symmetric key
   IV = lea.get_random_bits(128) # initial vector\
   s = 64  # block size for encryption/decryption
   # print('Alice and Bob agreed on symmetric key:', k)
   
   old_plaintext = 'Hi Bob! sup?'
   
   result =(bin(int(get_ascii_values(old_plaintext))))[2:]
   plaintext = result
   if (len(result) < 128):
       plaintext=(result).zfill(128)
 
   #################################### LEA ####################################
   # encrypt plaintext using symmetric key
   ciphertext = OFB.encryption_decryption_LEA_OFB(message=plaintext, key=k, initialV=IV, block_size=s)
   print('Plaintext encrypted, now encrypt symmetric key using EC El Gamal')
   print('Ciphertext:', ciphertext)
   print('-------------------------------------')

   #################################### EC El Gamal ####################################
   # now encrypt the symmetric key using EC El gamal
   symmetricKey = int(k,2)  # change value from str to int
   y1x,y2x = gm.encrypt(symmetricKey) # encrypt the symmetric key using EC ElGamal
   
   print('-------------------------------------')
   print('Symmetric key encrypted, now add digital signature using RSA')
   print('-------------------------------------')

   #################################### RSA ##################################
   # Initialize keys
   rsa.primefiller()
   rsa.setkeys()
   
   # in the following part, we should add a digital signature using RSA
   # step 1: hash the ciphertext
   # step 2: encrypt the hashed ciphertext
   # step 3: attach signature and send to Bob
   # if Bob got the same values then he can make sure that the message sent is indeed from alice
   
   # 1 hash the ciphertext
   hashed_ciphertext = hash(ciphertext)
   # 2 encrypt hashed ciphertext using rsa
   DS_Encrypted = rsa.encoder(str(hashed_ciphertext))
   # 3 concat ciphertext + encrypted hash , should add a flag in the middle 
   Signed_message = ciphertext + 'flag'+ str(DS_Encrypted)
   print('Digital signature added')
   
   ###########################################################################
    # now Alice's part is over, Bob's part is up
   print('Email is being sent now')
   print('-------------------------------------')
   print('Bob received the email, first he need to verify that the message was not tampered')
   
   # verification part,first split the digital signature from the ciphertext
   # this part is all about restoring the digital signature in it's list form to decrypt it
   signature = Signed_message.split('flag')
   l = []
   l.append(signature[1])
   x = (l[0][1:])[:-1]
   y = [ int(item) for item in x.split(', ')]
   # digital signature restored
   # now decrypt digital signature, aka hashed ciphertext
   hashed_ciphertext = rsa.decoder(y)
   
   # now has the ciphertext
   hashCipher2 = str(hash(signature[0]))
   print('Verifying sender ......')
   print('Decrypted RSA signature:', hashed_ciphertext)
   print('Hashed ciphertext:', hashCipher2)
   if (hashCipher2!=hashed_ciphertext):
       print('Verification Failed!\nThis message could have been tampered!')
       sys.exit()
       
   print('The signature is valid. Sender authenication successful')
   
   #################################### Decryption ##################################
   # start by decrypting the symmetric key
   decrypted_symmetricKey = gm.decrypt(y1x, y2x)
   # now decrypt the ciphertext with the symmetric key
   decrypted_symmetricKey = (bin(decrypted_symmetricKey))[2:]
   decrypted = OFB.encryption_decryption_LEA_OFB(message=ciphertext, key=decrypted_symmetricKey, initialV=IV, block_size=s)

   print('-------------------------------------')
   print('Alice sent:', old_plaintext)
   print('-------------------------------------')
   print('Ciphertext + RSA digital signature:', Signed_message)
   print('-------------------------------------')
   print('Bob received:', get_characters_from_ascii_values(str(int(decrypted,2))))
   print('-------------------------------------')


if __name__ == "__main__":
    main()
