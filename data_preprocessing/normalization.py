import re



def remove_diacritics(text):
    arabic_diacritics = re.compile(r"""
        ّ|
        َ|
        ً|
        ُ|
        ٌ|
        ِ|
        ٍ|
        ْ|
        ـ
    """, re.VERBOSE)

    return re.sub(arabic_diacritics, '', str(text))

def alif_normalization(query):
    query = str(query).replace("إ", "ا").replace("أ", "ا").replace("آ", "ا")
    return query

def fa_normalization(query):
    query = str(query).replace("ڤ", "ف")
    return query


def taa_normalization(query):
    if query.endswith(".") or query.endswith(",") or query.endswith("،"):
        query = query[:-1]
    if query.endswith("ة"):
        query = query[:-1] + "ه"
    query = query.replace("ة","ه")
    return query


def yaa_normalization(query):
    if query.endswith(".") or query.endswith(",") or query.endswith("،"):
        query = query[:-1]
    if query.endswith("ي"):
        query = query[:-1] + "ى"
    return query


def al_normalization(query):
    if query.strip().startswith("ال"):
        query = query[2:]
    return query


def ll_normalization(query):
    if query.strip().startswith("لل"):
        query = query[2:]
    return query

def arabic_normalization(query):
    """
    Normalize arabic words by unify 'أآإا','ي ى','ة ه' and removing 'ال'
    :param text: query.
    :return: normalized arabic query.
    """
    query = remove_diacritics(query)
    words = query.split()
    new_query = [alif_normalization(
        taa_normalization(
                fa_normalization(
                yaa_normalization(w)))) for w in words]

    new_query = " ".join(new_query)
    return new_query