import unicodedata


def clean_unicode(string):
    return unicodedata.normalize(
        'NFKD', string).encode('ascii', 'ignore')
