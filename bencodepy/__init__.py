from bencodepy.common import Bencached
from bencodepy.decoder import BencodeDecoder
from bencodepy.encoder import BencodeEncoder
from bencodepy.exceptions import BencodeDecodeError, BencodeEncodeError

try:
    from typing import Dict, List, Tuple, Deque, Union, TextIO, BinaryIO, Any
except ImportError:
    Dict = List = Tuple = Deque = Union = TextIO = BinaryIO = Any = None

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None

try:
    import pathlib
except ImportError:
    pathlib = None


__all__ = (
    'Bencached',
    'Bencode',
    'BencodeDecodeError',
    'BencodeDecoder',
    'BencodeEncodeError',
    'BencodeEncoder',
    'bencode',
    'bdecode',
    'bread',
    'bwrite',
    'encode',
    'decode'
)


class Bencode(object):
    def __init__(self, encoding=None, encoding_fallback=None, dict_ordered=False, dict_ordered_sort=False):
        self.decoder = BencodeDecoder(
            encoding=encoding,
            encoding_fallback=encoding_fallback,
            dict_ordered=dict_ordered,
            dict_ordered_sort=dict_ordered_sort
        )

        self.encoder = BencodeEncoder()

    def decode(self, value):
        return self.decoder.decode(value)

    def encode(self, value):
        return self.encoder.encode(value)

    def read(self, fd):
        raise NotImplementedError()

    def write(self, data, fd):
        raise NotImplementedError()


DEFAULT = Bencode()


def bencode(value):
    return DEFAULT.encode(value)


def bdecode(value):
    return DEFAULT.decode(value)


def bread(fd):
    return DEFAULT.read(fd)


def bwrite(data, fd):
    return DEFAULT.write(data, fd)


# Compatibility Proxies
encode = bencode
decode = bdecode
