# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by Petru Paler

"""bencode.py - bencode encoder + decoder."""

from bencode.common import Bencached
from bencode.decoder import BencodeDecoder
from bencode.encoder import BencodeEncoder
from bencode.exceptions import BencodeDecodeError

try:
    import pathlib
except ImportError:
    pathlib = None

__all__ = (
    'Bencached',
    'Bencode',
    'BencodeDecoder',
    'BencodeDecodeError',
    'BencodeEncoder',
    'bencode',
    'bdecode',
    'bread',
    'bwrite',
    'encode',
    'decode'
)


class Bencode(object):
    def __init__(self):
        self.decoder = BencodeDecoder()
        self.encoder = BencodeEncoder()

    def decode(self, value):
        return self.decoder.decode(value)

    def encode(self, value):
        return self.encoder.encode(value)


DEFAULT = Bencode()


def bencode(value):
    # type: (Union[Tuple, List, OrderedDict, Dict, bool, int, str, bytes]) -> bytes
    """
    Encode ``value`` into the bencode format.

    :param value: Value
    :type value: object

    :return: Bencode formatted string
    :rtype: str
    """
    return DEFAULT.encode(value)


def bdecode(value):
    # type: (bytes) -> Union[Tuple, List, OrderedDict, bool, int, str, bytes]
    """
    Decode bencode formatted byte string ``value``.

    :param value: Bencode formatted string
    :type value: bytes

    :return: Decoded value
    :rtype: object
    """
    return DEFAULT.decode(value)


def bread(fd):
    # type: (Union[bytes, str, pathlib.Path, pathlib.PurePath, TextIO, BinaryIO]) -> bytes
    """Return bdecoded data from filename, file, or file-like object.

    if fd is a bytes/string or pathlib.Path-like object, it is opened and
    read, otherwise .read() is used. if read() not available, exception
    raised.
    """
    if isinstance(fd, (bytes, str)):
        with open(fd, 'rb') as fd:
            return bdecode(fd.read())
    elif pathlib is not None and isinstance(fd, (pathlib.Path, pathlib.PurePath)):
        with open(str(fd), 'rb') as fd:
            return bdecode(fd.read())
    else:
        return bdecode(fd.read())


def bwrite(data,  # type: Union[Tuple, List, OrderedDict, Dict, bool, int, str, bytes]
           fd     # type: Union[bytes, str, pathlib.Path, pathlib.PurePath, TextIO, BinaryIO]
           ):
    # type: (...) -> None
    """Write data in bencoded form to filename, file, or file-like object.

    if fd is bytes/string or pathlib.Path-like object, it is opened and
    written to, otherwise .write() is used. if write() is not available,
    exception raised.
    """
    if isinstance(fd, (bytes, str)):
        with open(fd, 'wb') as fd:
            fd.write(bencode(data))
    elif pathlib is not None and isinstance(fd, (pathlib.Path, pathlib.PurePath)):
        with open(str(fd), 'wb') as fd:
            fd.write(bencode(data))
    else:
        fd.write(bencode(data))


# Compatibility Proxies
encode = bencode
decode = bdecode
