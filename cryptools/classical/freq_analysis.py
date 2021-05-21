from scipy.stats import chi2

mono_exp = {'e': 0.12575645, 't': 0.09085226, 'a': 0.08000395, 'o': 0.0759127, 'i': 0.06920007, 'n': 0.06903785, 's': 0.0634088, 'h': 0.06236609, 'r': 0.05959034, 'd': 0.04317924, 'l': 0.04057231, 'u': 0.02841783, 'c': 0.02575785, 'm': 0.02560994, 'f': 0.02350463, 'w': 0.02224893, 'g': 0.01982677, 'y': 0.01900888, 'p': 0.01795742, 'b': 0.01535701, 'v': 0.00981717, 'k': 0.00739906, 'x': 0.00179556, 'j': 0.00145188, 'q': 0.00117571, 'z': 0.0007913}

bi_exp = {'th': 0.03882543, 'he': 0.03681391, 'in': 0.02283899, 'er': 0.02178042, 'an': 0.0214046, 're': 0.01749394, 'nd': 0.01571977, 'on': 0.01418244, 'en': 0.01383239, 'at': 0.01335523, 'ou': 0.01285484, 'ed': 0.01275779, 'ha': 0.01274742, 'to': 0.01169655, 'or': 0.01151094, 'it': 0.01134891, 'is': 0.01109877, 'hi': 0.01092302, 'es': 0.01092301, 'ng': 0.01053385}

tri_exp = {'the': 0.03508232, 'and': 0.01593878, 'ing': 0.01147042, 'her': 0.00822444, 'hat': 0.00650715, 'his': 0.00596748, 'tha': 0.00593593, 'ere': 0.00560594, 'for': 0.00555372, 'ent': 0.00530771, 'ion': 0.00506454, 'ter': 0.00461099, 'was': 0.00460487, 'you': 0.00437213, 'ith': 0.0043125, 'ver': 0.00430732, 'all': 0.00422758, 'wit': 0.0039729, 'thi': 0.00394796, 'tio': 0.00378058}

alph = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

def is_english(m, pval=0.001):
    return all(list(map(lambda x: x > pval, chi2_pvals(m))))

def chi2_pvals(m, minlen=10):
    assert(len(m) >= minlen)
    m = trim(m).lower()
    mono_freq = _monogram(m)
    mono_pval = _pval(mono_freq, mono_exp, df=26-1)
    bi_freq = _bigram(m)
    bi_pval = _pval(bi_freq, bi_exp, df=26**2 - 1)
    tri_freq = _trigram(m)
    tri_pval = _pval(tri_freq, tri_exp, df=26**3 - 1)
    return mono_pval, bi_pval, tri_pval

def _monogram(m):
    res = {}
    for c in m:
        if not c in res:
            res[c] = 1
        else:
            res[c] += 1
    return res

def _bigram(m):
    res = {}
    for i in range(len(m) - 1):
        c = m[i:i+2]
        if not c in res:
            res[c] = 1
        else:
            res[c] += 1
    return res

def _trigram(m):
    res = {}
    for i in range(len(m) - 2):
        c = m[i:i+3]
        if not c in res:
            res[c] = 1
        else:
            res[c] += 1
    return res

def _pval(freq, exp, df=25):
    stat = 0.0
    total_freq = 0
    for c in freq:
        total_freq += freq[c]
    for c in freq:
        if c in exp:
            exp_freq = exp[c] * total_freq
            stat += (freq[c] - exp_freq) ** 2 / exp_freq
    return chi2.sf(stat, df=df)

def trim(m):
    res = []
    for c in m:
        if c in alph:
            res.append(c)
    return ''.join(res)

assert(is_english('I really really like fruits'))
assert(not is_english('I really really like fruits ZZXX'))
