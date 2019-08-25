from Crypto.Cipher import AES
from random import randint
from functools import reduce
from .xor import xor

def generate_key(key_size=16):
	return bytes([randint(0,255) for _ in range(key_size)])

def pad(data, block_size=16, style='pkcs7'):
	assert block_size < 256
	assert style == 'pkcs7'
	num_remaining = block_size - len(data) % block_size
	return data + (chr(num_remaining) * num_remaining).encode('utf-8')

# Unsafe
def unpad(data, block_size=16, style='pkcs7'):
	assert(block_size < 256)
	assert(style == 'pkcs7')
	assert(not (len(data) % block_size))
	last_byte = data[-1]
	assert(last_byte <= block_size)
	return data[:-last_byte]

def aes_ecb_encrypt(plaintext, key, padding=True):
	cipher = AES.new(key, AES.MODE_ECB)
	if padding:
		plaintext = pad(plaintext)
	return cipher.encrypt(plaintext)

def aes_ecb_decrypt(ciphertext, key, unpadding=True):
	cipher = AES.new(key, AES.MODE_ECB)
	res = cipher.decrypt(ciphertext)
	if unpadding:
		return unpad(res)
	else:
		return res

def aes_cbc_encrypt(plaintext, key, iv):
	cipher = AES.new(key, AES.MODE_ECB)
	m = pad(plaintext)
	blocks = [m[i:i+16] for i in range(0, len(m), 16)]
	c_blocks = []
	for block in blocks:	
		iv = cipher.encrypt(xor(block, iv))
		c_blocks.append(iv)
	return reduce(lambda x,y: x+y, c_blocks)

def aes_cbc_decrypt(ciphertext, key, iv):
	c = ciphertext
	cipher = AES.new(key, AES.MODE_ECB)
	c_blocks = [c[i:i+16] for i in range(0, len(c), 16)][::-1]
	c_blocks.append(iv)
	m_blocks = []
	for i in range(len(c_blocks) - 1):
		c_block = c_blocks[i]
		m_blocks.append(xor(cipher.decrypt(c_block), c_blocks[i+1]))
	return reduce(lambda x,y: x+y, m_blocks[::-1])

def aes_ctr_encrypt(plaintext, key, nonce=b'\x00\x00\x00\x00\x00\x00\x00\x00', byteorder='little'):
	cipher = AES.new(key, AES.MODE_ECB)
	m_length = len(plaintext)
	counter = 0
	keystream = b''
	while len(keystream) < m_length:
		keystream += cipher.encrypt(nonce + counter.to_bytes(8, byteorder=byteorder))
		counter += 1
	return xor(plaintext, keystream[:m_length])

def aes_ctr_decrypt(ciphertext, key, nonce=b'\x00\x00\x00\x00\x00\x00\x00\x00', byteorder='little'):
	return aes_ctr_encrypt(ciphertext, key, nonce, byteorder)