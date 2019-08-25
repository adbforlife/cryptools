from Crypto.Cipher import AES
from random import randint
from functools import reduce
from .xor import xor
from ..util.pad import pad, unpads

def aes_ecb_encrypt(m, key, padding=True):
    cipher = AES.new(key, AES.MODE_ECB)
    if padding:
        m = pad(m)
    return cipher.encrypt(m)

def aes_ecb_decrypt(c, key, padding=True):
    cipher = AES.new(key, AES.MODE_ECB)
    res = cipher.decrypt(c)
    if padding:
        return unpad(res)
    else:
        return res

def aes_cbc_encrypt(m, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    m = pad(m)
    blocks = [m[i:i+16] for i in range(0, len(m), 16)]
    c_blocks = []
    for block in blocks:    
        iv = cipher.encrypt(xor(block, iv))
        c_blocks.append(iv)
    return reduce(lambda x,y: x+y, c_blocks)

def aes_cbc_decrypt(c, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    c_blocks = [c[i:i+16] for i in range(0, len(c), 16)][::-1]
    c_blocks.append(iv)
    m_blocks = []
    for i in range(len(c_blocks) - 1):
        c_block = c_blocks[i]
        m_blocks.append(xor(cipher.decrypt(c_block), c_blocks[i+1]))
    return reduce(lambda x,y: x+y, m_blocks[::-1])

def aes_ctr_encrypt(m, key, nonce=b'\x00\x00\x00\x00\x00\x00\x00\x00', byteorder='little'):
    cipher = AES.new(key, AES.MODE_ECB)
    m_length = len(m)
    counter = 0
    keystream = b''
    while len(keystream) < m_length:
        keystream += cipher.encrypt(nonce + counter.to_bytes(8, byteorder=byteorder))
        counter += 1
    return xor(m, keystream[:m_length])

def aes_ctr_decrypt(c, key, nonce=b'\x00\x00\x00\x00\x00\x00\x00\x00', byteorder='little'):
    return aes_ctr_encrypt(c, key, nonce, byteorder)
