from .cipher import generate_key
from statistics import mode

from .attacks.attack_repeating_key_xor import guess_key_size, guess_key

# Not 100% correct since \x02\x02 is also valid
def cbc_padding_oracle(c, iv, valid_checker):
	c_blocks = [iv] + [c[i:i+16] for i in range(0,len(c),16)]
	m = b''
	for i in range(1, len(c_blocks)):
		c_block = c_blocks[i]
		correct_test_block = [0 for _ in range(16)]

		# Give multiple tries to increase likelihood
		last_byte_candidates = []
		for j in range(5):
			test_block = generate_key()
			while not valid_checker(c_block, test_block):
				test_block = generate_key()
			last_byte_candidates.append(test_block[15] ^ 1)
		correct_test_block[15] = mode(last_byte_candidates)

		for j in range(1,16):
			xored_correct_test_block = list(map(lambda x: x ^ (j+1), correct_test_block))
			test_block = generate_key(16-j) + bytes(xored_correct_test_block[16-j:])
			while not valid_checker(c_block, test_block):
				test_block = generate_key(16-j) + bytes(xored_correct_test_block[16-j:])
			correct_test_block[15-j] = test_block[15-j] ^ (j+1)
		m_block = bytes([c_blocks[i-1][k] ^ correct_test_block[k] for k in range(16)])
		m += m_block
	return m

def repeating_xor_guess_key(ciphertext, key_size=-1, alpha=0.000001, normal_rate=0.8):
	if key_size < 0:
		key_size = guess_key_size(ciphertext)
	return guess_key(ciphertext, key_size, alpha, normal_rate)