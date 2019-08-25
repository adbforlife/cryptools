def f(x,y,z):
    return (x & y) | ((0xFFFFFFFF ^ x) & z)

def g(x,y,z):
    return (x & y) | (x & z) | (y & z)

def h(x,y,z):
    return x ^ y ^ z

def md4(m, digest='hex'):
    if isinstance(m, str):
        m = m.encode('utf-8')

    A = 0x01234567
    B = 0x89ABCDEF
    C = 0XFEDCBA98
    D = 0X76543210
    
