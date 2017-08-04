#!/usr/bin/env python
# encoding: utf-8

"""bencode.py tests."""

from bencode import BTFailure, bencode, bdecode

import unittest


class KnownValues(unittest.TestCase):
    """
    Test known bencode values.

    Example values partially taken from http://en.wikipedia.org/wiki/Bencode, test case inspired
    by Mark Pilgrim's examples: http://diveintopython.org/unit_testing/romantest.html
    """

    knownValues = (
        (0, 'i0e'.encode('utf-8')),
        (1, 'i1e'.encode('utf-8')),
        (10, 'i10e'.encode('utf-8')),
        (42, 'i42e'.encode('utf-8')),
        (-42, 'i-42e'.encode('utf-8')),
        (True, 'i1e'.encode('utf-8')),
        (False, 'i0e'.encode('utf-8')),
        ('spam', '4:spam'.encode('utf-8')),
        ('parrot sketch', '13:parrot sketch'.encode('utf-8')),
        (['parrot sketch', 42], 'l13:parrot sketchi42ee'.encode('utf-8')),
        ({
            'foo': 42,
            'bar': 'spam'
        }, 'd3:bar4:spam3:fooi42ee'.encode('utf-8')),
    )

    def testBencodeKnownValues(self):
        """Encode should give known result with known input."""
        for plain, encoded in self.knownValues:
            result = bencode(plain)
            self.assertEqual(encoded, result)

    def testBdecodeKnownValues(self):
        """Decode should give known result with known input."""
        for plain, encoded in self.knownValues:
            result = bdecode(encoded)
            self.assertEqual(plain, result)

    def testRoundtripEncoded(self):
        """Consecutive calls to decode and encode should deliver the original data again."""
        for plain, encoded in self.knownValues:
            result = bdecode(encoded)
            self.assertEqual(encoded, bencode(result))

    def testRoundtripDecoded(self):
        """Consecutive calls to encode and decode should deliver the original data again."""
        for plain, encoded in self.knownValues:
            result = bencode(plain)
            self.assertEqual(plain, bdecode(result))


class IllegalValues(unittest.TestCase):
    """Test handling of illegal values."""

    # TODO: BTL implementation currently chokes on this type of input
    # def testFloatRaisesIllegalForEncode(self):
    #     """ floats cannot be encoded. """
    #     self.assertRaises(BTFailure, bencode, 1.0)

    def testNonStringsRaiseIllegalInputForDecode(self):
        """Ensure non-strings raise an exception."""
        # TODO: BTL implementation currently chokes on this type of input
        # self.assertRaises(BTFailure, bdecode, 0)
        # self.assertRaises(BTFailure, bdecode, None)
        # self.assertRaises(BTFailure, bdecode, 1.0)
        self.assertRaises(BTFailure, bdecode, [1, 2])
        self.assertRaises(BTFailure, bdecode, {'foo': 'bar'})

    def testRaiseIllegalInputForDecode(self):
        """Illegally formatted strings should raise an exception when decoded."""
        self.assertRaises(BTFailure, bdecode, "foo")
        self.assertRaises(BTFailure, bdecode, "x:foo")
        self.assertRaises(BTFailure, bdecode, "x42e")


class Dictionaries(unittest.TestCase):
    """Test handling of dictionaries."""

    def testSortedKeysForDicts(self):
        """Ensure the keys of a dictionary are sorted before being encoded."""
        encoded = bencode({'zoo': 42, 'bar': 'spam'})

        self.assertTrue(encoded.index(b'zoo') > encoded.index(b'bar'))

    def testNestedDictionary(self):
        """Test the handling of nested dicts."""
        self.assertEqual(
            bencode({'foo': 42, 'bar': {'sketch': 'parrot', 'foobar': 23}}),
            'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'.encode('utf-8')
        )
