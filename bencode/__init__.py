from bencode.BTL import BTFailure
from bencode.exceptions import BencodeDecodeError

from bencodepy import Bencached, Bencode

__all__ = (
    'BTFailure',
    'Bencached',
    'BencodeDecodeError',
    'bencode',
    'bdecode',
    'bread',
    'bwrite',
    'encode',
    'decode'
)

DEFAULT = Bencode(
    encoding='utf-8',
    encoding_fallback='value',
    dict_ordered=True,
    dict_ordered_sort=True
)

bdecode = DEFAULT.decode
bencode = DEFAULT.encode
bread = DEFAULT.read
bwrite = DEFAULT.write

decode = bdecode
encode = bencode
