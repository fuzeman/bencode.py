from bencodepy import bdecode, bencode, Bencached, BencodeDecodeError

from collections import OrderedDict
import pytest


def test_decode():
    with pytest.raises(BencodeDecodeError):
        bdecode([1, 2])

    with pytest.raises(BencodeDecodeError):
        bdecode({'foo': 'bar'})

    with pytest.raises(BencodeDecodeError):
        bdecode('foo')

    with pytest.raises(BencodeDecodeError):
        bdecode('x:foo')

    with pytest.raises(BencodeDecodeError):
        bdecode('x42e')


def test_decode_bytes():
    assert bdecode(b'1:\x9c') == '\x9c'


def test_decode_dict():
    assert bdecode(b'd4:name7:bencodee') == {'name': 'bencode'}
    assert bdecode(b'd5:majori2e5:minori7e4:name6:Pythone') == {'name': 'Python', 'major': 2, 'minor': 7}


def test_decode_int():
    assert bdecode(b'i1e') == 1
    assert bdecode(b'i0e') == 0
    assert bdecode(b'i-1e') == -1

    with pytest.raises(BencodeDecodeError):
        bdecode(b'ie')

    with pytest.raises(BencodeDecodeError):
        bdecode(b'i03e')

    with pytest.raises(BencodeDecodeError):
        bdecode(b'i-0e')


def test_decode_list():
    assert bdecode(b'l7:bencodee') == ['bencode']
    assert bdecode(b'l6:Pythoni2ei7ee') == ['Python', 2, 7]


def test_decode_string():
    assert bdecode(b'7:bencode') == 'bencode'
    assert bdecode(b'10:Python 2.7') == 'Python 2.7'

    with pytest.raises(BencodeDecodeError):
        bdecode(b'00:bencode')


def test_encode_bencached():
    assert bencode([Bencached(bencode('test'))]) == 'l4:teste'


def test_encode_bool():
    assert bencode(True) == b'i1e'
    assert bencode(False) == b'i0e'


def test_encode_bytes():
    assert bencode('\x9c') == b'1:\x9c'


def test_encode_dict():
    assert bencode({'name': 'bencode'}) == b'd4:name7:bencodee'
    assert bencode({'name': 'Python', 'major': 2, 'minor': 7}) == b'd5:majori2e5:minori7e4:name6:Pythone'


def test_encode_dict_nested():
    assert bencode({'foo': 42, 'bar': {'sketch': 'parrot', 'foobar': 23}}) == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'


def test_encode_dict_ordered():
    d = OrderedDict()
    d['name'] = 'bencode'

    assert bencode(d) == b'd4:name7:bencodee'

    d = OrderedDict()
    d['name'] = 'Python'
    d['major'] = 2
    d['minor'] = 7

    assert bencode(d) == b'd4:name6:Python5:majori2e5:minori7ee'


def test_encode_dict_sorted():
    encoded = bencode({'zoo': 42, 'bar': 'spam'})

    assert encoded.index(b'zoo') > encoded.index(b'bar')


def test_encode_dict_unicode():
    assert bencode({u'foo': 42, 'bar': {u'sketch': u'parrot', 'foobar': 23}}) == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'


def test_encode_int():
    assert bencode(1) == b'i1e'
    assert bencode(0) == b'i0e'
    assert bencode(-1) == b'i-1e'


def test_encode_list():
    assert bencode(['bencode']) == b'l7:bencodee'
    assert bencode(['Python', 2, 7]) == b'l6:Pythoni2ei7ee'


def test_encode_string():
    assert bencode('bencode') == b'7:bencode'
    assert bencode('Python 2.7') == b'10:Python 2.7'


def test_encode_tuple():
    assert bencode(('bencode',)) == b'l7:bencodee'
    assert bencode(('Python', 2, 7)) == b'l6:Pythoni2ei7ee'
