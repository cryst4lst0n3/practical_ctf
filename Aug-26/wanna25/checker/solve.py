nonce = [ord('E')]*12
nonce = bytes(nonce)
key = [0XAA] * 32
key = bytes(key)
enc = [
    0xfc, 0x76, 0xd4, 0x09, 0xa3, 0xd8, 0x50, 0x2f, 0xb9, 0xd7, 0xba, 0xe0, 0xb0, 0x34,0xb2
]
enc = bytes(enc)

from Crypto.Cipher import ChaCha20

Cipher = ChaCha20.new(key=key, nonce=nonce)
enc = Cipher.decrypt(enc)

print(enc)


