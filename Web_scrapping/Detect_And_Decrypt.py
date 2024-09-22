import base64
import hashlib
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import os

# AES Decryption function
def decrypt_aes(ciphertext, key, iv):
    try:
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
        decrypted_data = decrypted_data[:-decrypted_data[-1]]  # Remove padding
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting AES: {e}")
        return None

# RSA Decryption function
def decrypt_rsa(ciphertext, private_key_path):
    try:
        with open(private_key_path, 'r') as key_file:
            private_key = RSA.importKey(key_file.read())
            cipher_rsa = PKCS1_OAEP.new(private_key)
            decrypted_data = cipher_rsa.decrypt(base64.b64decode(ciphertext))
            return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting RSA: {e}")
        return None

# Hash cracking using dictionary attack
def crack_hash(hash_value, hash_type='md5'):
    try:
        with open("common_passwords.txt", "r") as file:
            for password in file:
                password = password.strip()
                if hash_type == 'md5':
                    hashed = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == 'sha256':
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                
                if hashed == hash_value:
                    print(f"Cracked hash: {password}")
                    return password
        print(f"Could not crack {hash_type} hash.")
    except Exception as e:
        print(f"Error cracking hash: {e}")
    return None

# Base64 Decoder
def decode_base64(encoded_data):
    try:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        print(f"Base64 decoded: {decoded_data}")
        return decoded_data
    except Exception as e:
        print(f"Base64 decode error: {e}")
        return None

# Encryption Detection and Decryption Program
def detect_and_decrypt(encrypted_data, aes_key=None, aes_iv=None, rsa_private_key_path=None):
    try:
        # Try Base64 decoding
        print("Attempting Base64 decoding...")
        decoded_data = decode_base64(encrypted_data)
        if decoded_data:
            return decoded_data
    except:
        print("Not Base64 encoded.")

    # Try AES decryption if key and IV are provided
    if aes_key and aes_iv:
        print("Attempting AES decryption...")
        decrypted_data = decrypt_aes(encrypted_data, aes_key, aes_iv)
        if decrypted_data:
            print(f"AES Decrypted: {decrypted_data}")
            return decrypted_data

    # Try RSA decryption if a private key is provided
    if rsa_private_key_path:
        print("Attempting RSA decryption...")
        decrypted_data = decrypt_rsa(encrypted_data, rsa_private_key_path)
        if decrypted_data:
            print(f"RSA Decrypted: {decrypted_data}")
            return decrypted_data

    # Check for common hash types (MD5, SHA-256)
    print("Checking for common hash types (MD5, SHA-256)...")
    if len(encrypted_data) == 32:  # MD5 is 32 characters long
        print("Detected potential MD5 hash.")
        return crack_hash(encrypted_data, 'md5')
    elif len(encrypted_data) == 64:  # SHA-256 is 64 characters long
        print("Detected potential SHA-256 hash.")
        return crack_hash(encrypted_data, 'sha256')

    print("Unable to decrypt or detect data format.")
    return None

# Example usage
if __name__ == "__main__":
    # Example encrypted data (replace with actual values)
    encrypted_text = "YOUR_ENCRYPTED_DATA_HERE"
    aes_key = "YOUR_AES_KEY_16_CHARACTERS"  # For AES decryption
    aes_iv = "YOUR_AES_IV_16_CHARACTERS"  # For AES decryption
    rsa_private_key_file = "path_to_your_private_key.pem"  # For RSA decryption

    result = detect_and_decrypt(encrypted_text, aes_key, aes_iv, rsa_private_key_file)
    if result:
        print(f"Decrypted result: {result}")
    else:
        print("Failed to decrypt the data.")
