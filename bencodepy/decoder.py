from bencodepy.compat import to_binary
from bencodepy.exceptions import BencodeDecodeError
from collections import OrderedDict

ENCODING_FALLBACK_TYPES = ('key', 'value')
STRING_TYPES = (b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9')

class BencodeDecoder(object):
    def __init__(self, encoding=None, encoding_fallback=None, dict_ordered=False, dict_ordered_sort=False):
        self.encoding = encoding
        self.dict_ordered = dict_ordered
        self.dict_ordered_sort = dict_ordered_sort

        if dict_ordered_sort and not dict_ordered:
            raise ValueError(
                'Invalid value for "dict_ordered_sort" ("dict_ordered" must also be enabled)'
            )

        if encoding_fallback is not None and encoding_fallback not in ENCODING_FALLBACK_TYPES + ('all',):
            raise ValueError(
                'Invalid value for "encoding_fallback" (expected "all", "key", "value", or None)'
            )

        self.encoding_fallback = tuple([
            value for value in ENCODING_FALLBACK_TYPES
            if value == encoding_fallback or encoding_fallback == 'all'
        ])

        self._decode_handlers = {
            b'd': self._decode_dict,
            b'i': self._decode_int,
            b'l': self._decode_list
        }

    def decode(self, value):
        decoded, length = self._decode(value)

        # Ensure entire value was decoded
        if length < len(value):
            raise BencodeDecodeError("invalid bencoded value (trailing data found: %s)" % (value[length:],))

        return decoded

    def _decode(self, value):
        try:
            value = to_binary(value)

            # Decode value
            if value[0] in STRING_TYPES:
                decoded, length = self._decode_string(value)
            else:
                decoded, length = self._decode_handlers[value[0]](value)
        except Exception, e:
            raise BencodeDecodeError('not a valid bencoded string', e)

        return decoded, length

    def _decode_dict(self, value):
        pos = 1

        if self.dict_ordered:
            result = OrderedDict()
        else:
            result = {}

        while value[pos] != b'e':
            key, length = self._decode_string(value[pos:], kind='key')
            pos += length

            result[key], length = self._decode(value[pos:])
            pos += length

        if self.dict_ordered_sort:
            result = OrderedDict(sorted(result.items()))

        return result, pos + 1

    def _decode_int(self, value):
        end = value.index('e', 2)

        if value[1] == b'-':
            if value[2] == b'0':
                raise ValueError
        elif value[1] == b'0' and end > 2:
            raise ValueError

        return int(value[1:end]), end + 1

    def _decode_list(self, value):
        result = []
        pos = 1

        while value[pos] != b'e':
            decoded, length = self._decode(value[pos:])
            result.append(decoded)
            pos += length

        return result, pos + 1

    def _decode_string(self, value, kind='value'):
        pos = value.index(':')
        length = int(value[0:pos])

        if value[0] == b'0' and pos != 1:
            raise ValueError

        start = pos + 1
        value = value[start:start + length]

        if self.encoding:
            try:
                return value.decode(self.encoding), 1 + pos + length
            except UnicodeDecodeError:
                if kind not in self.encoding_fallback:
                    raise

        return bytes(value), 1 + pos + length
