#!/usr/bin/env python
# encoding: utf-8

"""bencode.py tests."""

from bencodepy import Bencached, BencodeDecodeError, bencode, bdecode
import pytest

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None


VALUES = [
    (0, b'i0e'),
    (1, b'i1e'),
    (10, b'i10e'),
    (42, b'i42e'),
    (-42, b'i-42e'),
    (True, b'i1e'),
    (False, b'i0e'),
    (b'spam', b'4:spam'),
    (b'parrot sketch', b'13:parrot sketch'),
    ([b'parrot sketch', 42], b'l13:parrot sketchi42ee'),
    ({b'foo': 42, b'bar': b'spam'}, b'd3:bar4:spam3:fooi42ee')
]

if OrderedDict is not None:
    VALUES.append((OrderedDict((
        (b'bar', b'spam'),
        (b'foo', 42)
    )), b'd3:bar4:spam3:fooi42ee'))

ENCODE = VALUES

DECODE = VALUES + [
    (0, 'i0e'),
    ([b'parrot sketch', 42], 'l13:parrot sketchi42ee'),
]


def test_encode():
    """Encode should give known result with known input."""
    for plain, encoded in ENCODE:
        assert encoded == bencode(plain)


def test_encode_bencached():
    """Ensure Bencached objects can be encoded."""
    assert bencode([Bencached(bencode('test'))]) == b'l4:teste'


def test_encode_bytes():
    """Ensure bytes can be encoded."""
    assert bencode(b'\x9c') == b'1:\x9c'


def test_decode():
    """Decode should give known result with known input."""
    for plain, encoded in DECODE:
        assert plain == bdecode(encoded)


def test_decode_bytes():
    """Ensure bytes can be decoded."""
    assert bdecode(b'1:\x9c') == b'\x9c'


def test_decode_dict():
    """Ensure bytes can be decoded."""
    value = bdecode('d5:title7:Examplee')

    # Ensure a dict is returned
    assert isinstance(value, dict)

    # Validate items
    assert value == {b'title': b'Example'}


def test_encode_roundtrip():
    """Consecutive calls to decode and encode should deliver the original data again."""
    for plain, encoded in ENCODE:
        assert encoded == bencode(bdecode(encoded))


def test_decode_roundtrip():
    """Consecutive calls to encode and decode should deliver the original data again."""
    for plain, encoded in VALUES:
        assert plain == bdecode(bencode(plain))


# TODO: BTL implementation currently chokes on this type of input
# def test_encode_float_error(self):
#     """ floats cannot be encoded. """
#     self.assertRaises(BTFailure, bencode, 1.0)

def test_decode_parameter():
    """Ensure non-strings raise an exception."""
    # TODO: BTL implementation currently chokes on this type of input
    # self.assertRaises(BTFailure, bdecode, 0)
    # self.assertRaises(BTFailure, bdecode, None)
    # self.assertRaises(BTFailure, bdecode, 1.0)
    with pytest.raises(BencodeDecodeError):
        bdecode([1, 2])

    with pytest.raises(BencodeDecodeError):
        bdecode({'foo': 'bar'})


def test_decode_errors():
    """Illegally formatted strings should raise an exception when decoded."""
    with pytest.raises(BencodeDecodeError):
        bdecode("foo")

    with pytest.raises(BencodeDecodeError):
        bdecode("x:foo")

    with pytest.raises(BencodeDecodeError):
        bdecode("x42e")


def test_dictionary_sorted():
    """Ensure the keys of a dictionary are sorted before being encoded."""
    encoded = bencode({'zoo': 42, 'bar': 'spam'})

    assert encoded.index(b'zoo') > encoded.index(b'bar')


def test_dictionary_unicode():
    """Test the handling of unicode in dictionaries."""
    encoded = bencode({u'foo': 42, 'bar': {u'sketch': u'parrot', 'foobar': 23}})

    assert encoded == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'.encode('utf-8')


def test_dictionary_nested():
    """Test the handling of nested dictionaries."""
    encoded = bencode({'foo': 42, 'bar': {'sketch': 'parrot', 'foobar': 23}})

    assert encoded == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'.encode('utf-8')
