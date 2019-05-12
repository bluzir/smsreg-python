import codecs


def prepare_dict(k, v):
    k = codecs.decode(k.encode('utf-8'), 'hex').decode('utf-8')
    v = codecs.decode(v.encode('utf-8'), 'hex').decode('utf-8')
    return {k: v}

