#!/usr/bin/env python
# encoding: utf-8

"""bencode.py tests."""

from bencode import Bencached, BTFailure, bencode, bdecode

import pytest
import sys

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None


VALUES = [
    (0, 'i0e'),
    (1, 'i1e'),
    (10, 'i10e'),
    (42, 'i42e'),
    (-42, 'i-42e'),
    (True, 'i1e'),
    (False, 'i0e'),
    ('spam', '4:spam'),
    ('parrot sketch', '13:parrot sketch'),
    (['parrot sketch', 42], 'l13:parrot sketchi42ee'),
    ({'foo': 42, 'bar': 'spam'}, 'd3:bar4:spam3:fooi42ee')
]

if OrderedDict is not None:
    VALUES.append((OrderedDict((
        ('bar', 'spam'),
        ('foo', 42)
    )), 'd3:bar4:spam3:fooi42ee'))


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Requires: Python 3+")
def test_encode():
    """Encode should give known result with known input."""
    for plain, encoded in VALUES:
        assert encoded.encode('utf-8') == bencode(plain)


@pytest.mark.skipif(sys.version_info[0] != 2, reason="Requires: Python 2")
def test_encode_py2():
    """Encode should give known result with known input."""
    for plain, encoded in VALUES:
        assert encoded == bencode(plain)


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Requires: Python 3+")
def test_encode_bencached():
    """Ensure Bencached objects can be encoded."""
    assert bencode([Bencached(bencode('test'))]) == b'l4:teste'


@pytest.mark.skipif(sys.version_info[0] != 2, reason="Requires: Python 2")
def test_encode_bencached_py2():
    """Ensure Bencached objects can be encoded."""
    assert bencode([Bencached(bencode('test'))]) == 'l4:teste'


def test_encode_bytes():
    """Ensure bytes can be encoded."""
    assert bencode(b'\x9c') == b'1:\x9c'


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Requires: Python 3+")
def test_decode():
    """Decode should give known result with known input."""
    for plain, encoded in VALUES:
        assert plain == bdecode(encoded.encode('utf-8'))


@pytest.mark.skipif(sys.version_info[0] != 2, reason="Requires: Python 2")
def test_decode_py2():
    """Decode should give known result with known input."""
    for plain, encoded in VALUES:
        assert plain == bdecode(encoded)


def test_decode_bytes():
    """Ensure bytes can be decoded."""
    assert bdecode(b'1:\x9c') == b'\x9c'


def test_decode_dict():
    """Ensure bytes can be decoded."""
    value = bdecode('d5:title7:Examplee')

    # Ensure OrderedDict is returned
    assert isinstance(value, OrderedDict)

    # Validate items
    assert value == {'title': 'Example'}


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Requires: Python 3+")
def test_encode_roundtrip():
    """Consecutive calls to decode and encode should deliver the original data again."""
    for plain, encoded in VALUES:
        assert encoded.encode('utf-8') == bencode(bdecode(encoded.encode('utf-8')))


@pytest.mark.skipif(sys.version_info[0] != 2, reason="Requires: Python 2")
def test_encode_roundtrip_py2():
    """Consecutive calls to decode and encode should deliver the original data again."""
    for plain, encoded in VALUES:
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
    with pytest.raises(BTFailure):
        bdecode([1, 2])

    with pytest.raises(BTFailure):
        bdecode({'foo': 'bar'})


def test_decode_errors():
    """Illegally formatted strings should raise an exception when decoded."""
    with pytest.raises(BTFailure):
        bdecode("foo")

    with pytest.raises(BTFailure):
        bdecode("x:foo")

    with pytest.raises(BTFailure):
        bdecode("x42e")


def test_dictionary_sorted():
    """Ensure the keys of a dictionary are sorted before being encoded."""
    encoded = bencode({'zoo': 42, 'bar': 'spam'})

    assert encoded.index(b'zoo') > encoded.index(b'bar')


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Requires: Python 3+")
def test_dictionary_unicode():
    """Test the handling of unicode in dictionaries."""
    encoded = bencode({u'foo': 42, 'bar': {u'sketch': u'parrot', 'foobar': 23}})

    assert encoded == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'.encode('utf-8')


@pytest.mark.skipif(sys.version_info[0] != 2, reason="Requires: Python 2")
def test_dictionary_unicode_py2():
    """Test the handling of unicode in dictionaries."""
    encoded = bencode({u'foo': 42, 'bar': {u'sketch': u'parrot', 'foobar': 23}})

    assert encoded == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'


@pytest.mark.skipif(sys.version_info[0] < 3, reason="Requires: Python 3+")
def test_dictionary_nested():
    """Test the handling of nested dictionaries."""
    encoded = bencode({'foo': 42, 'bar': {'sketch': 'parrot', 'foobar': 23}})

    assert encoded == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'.encode('utf-8')


@pytest.mark.skipif(sys.version_info[0] != 2, reason="Requires: Python 2")
def test_dictionary_nested_py2():
    """Test the handling of nested dictionaries."""
    encoded = bencode({'foo': 42, 'bar': {'sketch': 'parrot', 'foobar': 23}})

    assert encoded == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'
