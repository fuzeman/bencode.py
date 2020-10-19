from bencodepy.common import Bencached

from bencodepy.compat import PY2, to_binary
from bencodepy.exceptions import BencodeEncodeError

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None


class BencodeEncoder(object):
    def __init__(self):
        if PY2:
            from types import BooleanType, DictType, IntType, ListType, LongType, StringType, TupleType, UnicodeType

            self._encode_handlers = {
                Bencached: self._encode_bencached,
                BooleanType: self._encode_bool,
                DictType: self._encode_dict,
                IntType: self._encode_int,
                ListType: self._encode_list,
                LongType: self._encode_int,
                StringType: self._encode_bytes,
                TupleType: self._encode_list,
                UnicodeType: self._encode_string
            }

            if OrderedDict is not None:
                self._encode_handlers[OrderedDict] = self._encode_dict_ordered
        else:
            self._encode_handlers = {
                Bencached: self._encode_bencached,
                OrderedDict: self._encode_dict_ordered,
                bool: self._encode_bool,
                bytes: self._encode_bytes,
                dict: self._encode_dict,
                int: self._encode_int,
                list: self._encode_list,
                str: self._encode_string,
                tuple: self._encode_list
            }

    def encode(self, value):
        try:
            return self._encode_handlers[type(value)](value)
        except KeyError:
            raise BencodeEncodeError('Unsupported value type: %s' % (type(value),))

    def _encode_bencached(self, value):
        return value.bencoded

    def _encode_bool(self, value):
        return self._encode_int(1 if value else 0)

    def _encode_bytes(self, value):
        return str(len(value)).encode('utf-8') + b':' + value

    def _encode_dict(self, value):
        # Convert keys to binary and sort items by key
        items = [(to_binary(k), v) for k, v in value.items()]
        items.sort(key=lambda (k, v): k)

        # Encode dictionary
        return b'd' + ''.join([
            self.encode(key) + self.encode(value)
            for key, value in items
        ]) + b'e'

    def _encode_dict_ordered(self, value):
        # Convert keys to binary
        items = [(to_binary(k), v) for k, v in value.items()]

        # Encode dictionary
        return b'd' + ''.join([
            self.encode(key) + self.encode(value)
            for key, value in items
        ]) + b'e'

    def _encode_int(self, value):
        return b'i' + str(value).encode('utf-8') + b'e'

    def _encode_list(self, value):
        return b'l' + ''.join([
            self.encode(value)
            for value in value
        ]) + b'e'

    def _encode_string(self, value):
        return self._encode_bytes(value.encode('utf-8'))
