# Cipher
from .cipher.cipher_repeating_key_xor import repeating_xor
from .cipher.aes import (
    generate_key,
    aes_ecb_encrypt,
    aes_ecb_decrypt,
    aes_cbc_encrypt,
    aes_cbc_decrypt,
    aes_ctr_encrypt,
    aes_ctr_decrypt
)
from .cipher.rsa import (
    rsa_encrypt
    rsa_decrypt
)
from .cipher.xor import xor

# Hash
from .hash.sha1 import sha1

# Attack
from .attack.attack_single_byte_xor import (
    single_byte_xor,
    single_byte_xor_exlude_nonprintables
)
from .attack.attack_repeating_key_xor import (
    repeating_xor_guess_key_size,
    repeating_xor_guess_key
)

# PRNG
from .prng.mt19937 import (
    mt_init,
    seed,
    rand
)

from .util.pad import pad, unpad

if __name__ == '__main__':
    assert(sha1('adb') == 'fa1143dea12bffbbc1aa99d5da2ec811d63b5127')
    
    assert(rand() == 0xD091BB5C)
    assert(rand() == 0x22AE9EF6)
    seed(251)
    assert(rand() == 0xA33A7D59)
    assert(rand() == 0x8631FB6B)
    mt_init()
    seed(213)
    assert(rand() == 0x37EACD2B)
    assert(rand() == 0x956EB4E4)

    


