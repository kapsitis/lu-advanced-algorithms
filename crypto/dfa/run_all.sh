#!/bin/bash

# Create a random 128-bit AES key (do NOT look into this file until the end of DFA experiment!).
# openssl rand -hex 16 > aes_key.txt

# Store some 16-byte plaintext to a file.
echo '48656c6c6f20776f726c642120202020' | xxd -r -p > plaintext.txt

# Read the AES key into a variable
key=$(cat aes_key.txt)

# ECB-mode encryption
openssl enc -aes-128-ecb -in plaintext.txt -out ciphertext.bin -K "$key" -nopad

# Show the ciphertext as HEX.
xxd -p ciphertext.bin

