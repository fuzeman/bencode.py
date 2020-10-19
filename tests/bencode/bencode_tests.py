from bencode import bdecode, bencode, Bencached, BencodeDecodeError

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
    assert bdecode('1:\x9c') == '\x9c'


def test_decode_dict():
    assert bdecode('d4:name7:bencodee') == {'name': 'bencode'}
    assert bdecode('d5:majori2e5:minori7e4:name6:Pythone') == {'name': 'Python', 'major': 2, 'minor': 7}


def test_decode_int():
    assert bdecode('i1e') == 1
    assert bdecode('i0e') == 0
    assert bdecode('i-1e') == -1

    with pytest.raises(BencodeDecodeError):
        bdecode('ie')

    with pytest.raises(BencodeDecodeError):
        bdecode('i03e')

    with pytest.raises(BencodeDecodeError):
        bdecode('i-0e')


def test_decode_list():
    assert bdecode('l7:bencodee') == ['bencode']
    assert bdecode('l6:Pythoni2ei7ee') == ['Python', 2, 7]


def test_decode_string():
    assert bdecode('7:bencode') == 'bencode'
    assert bdecode('10:Python 2.7') == 'Python 2.7'

    with pytest.raises(BencodeDecodeError):
        bdecode('00:bencode')


def test_encode_bencached():
    assert bencode([Bencached(bencode('test'))]) == 'l4:teste'


def test_encode_bool():
    assert bencode(True) == 'i1e'.encode('utf-8')
    assert bencode(False) == 'i0e'.encode('utf-8')


def test_encode_bytes():
    assert bencode(b'\x9c') == b'1:\x9c'


def test_encode_dict():
    assert bencode({'name': 'bencode'}) == 'd4:name7:bencodee'.encode('utf-8')
    assert bencode({'name': 'Python', 'major': 2, 'minor': 7}) == 'd5:majori2e5:minori7e4:name6:Pythone'.encode('utf-8')


def test_encode_dict_nested():
    assert bencode({'foo': 42, 'bar': {'sketch': 'parrot', 'foobar': 23}}) == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'.encode('utf-8')


def test_encode_dict_ordered():
    d = OrderedDict()
    d['name'] = 'bencode'

    assert bencode(d) == 'd4:name7:bencodee'.encode('utf-8')

    d = OrderedDict()
    d['name'] = 'Python'
    d['major'] = 2
    d['minor'] = 7

    assert bencode(d) == 'd4:name6:Python5:majori2e5:minori7ee'.encode('utf-8')


def test_encode_dict_sorted():
    encoded = bencode({'zoo': 42, 'bar': 'spam'})

    assert encoded.index(b'zoo') > encoded.index(b'bar')


def test_encode_dict_unicode():
    assert bencode({u'foo': 42, 'bar': {u'sketch': u'parrot', 'foobar': 23}}) == 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'.encode('utf-8')


def test_encode_int():
    assert bencode(1) == 'i1e'.encode('utf-8')
    assert bencode(0) == 'i0e'.encode('utf-8')
    assert bencode(-1) == 'i-1e'


def test_encode_list():
    assert bencode(['bencode']) == 'l7:bencodee'.encode('utf-8')
    assert bencode(['Python', 2, 7]) == 'l6:Pythoni2ei7ee'.encode('utf-8')


def test_encode_string():
    assert bencode('bencode') == '7:bencode'.encode('utf-8')
    assert bencode('Python 2.7') == '10:Python 2.7'.encode('utf-8')


def test_encode_tuple():
    assert bencode(('bencode',)) == 'l7:bencodee'.encode('utf-8')
    assert bencode(('Python', 2, 7)) == 'l6:Pythoni2ei7ee'.encode('utf-8')
