#!/usr/bin/env python
# encoding: utf-8

"""bencode.py - file tests."""

from bencodepy import bread, bwrite
import os
import pytest
import sys

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
TEMP_DIR = os.path.join(os.path.dirname(__file__), '.tmp')

# Ensure temp directory exists
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


def test_read_file():
    """Test the reading of bencode files."""
    with open(os.path.join(FIXTURE_DIR, 'alpha'), 'rb') as fp:
        data = bread(fp)

        assert data == {b'foo': 42, b'bar': {b'sketch': b'parrot', b'foobar': 23}}


def test_read_path():
    """Test the reading of bencode paths."""
    data = bread(os.path.join(FIXTURE_DIR, 'alpha'))

    assert data == {b'foo': 42, b'bar': {b'sketch': b'parrot', b'foobar': 23}}


@pytest.mark.skipif(sys.version_info < (3, 4), reason="Requires: Python 3.4+")
def test_read_pathlib():
    """Test the reading of bencode paths."""
    from pathlib import Path

    data = bread(Path(FIXTURE_DIR, 'alpha'))

    assert data == {b'foo': 42, b'bar': {b'sketch': b'parrot', b'foobar': 23}}


def test_write_file():
    """Test the writing of bencode paths."""
    with open(os.path.join(TEMP_DIR, 'beta'), 'wb') as fp:
        bwrite(
            {b'foo': 42, b'bar': {b'sketch': b'parrot', b'foobar': 23}},
            fp
        )

    with open(os.path.join(TEMP_DIR, 'beta'), 'rb') as fp:
        assert fp.read() == b'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'


def test_write_path():
    """Test the writing of bencode files."""
    bwrite(
        {b'foo': 42, b'bar': {b'sketch': b'parrot', b'foobar': 23}},
        os.path.join(TEMP_DIR, 'beta')
    )

    with open(os.path.join(TEMP_DIR, 'beta'), 'rb') as fp:
        assert fp.read() == b'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'


@pytest.mark.skipif(sys.version_info < (3, 4), reason="Requires: Python 3.4+")
def test_write_pathlib():
    """Test the reading of bencode paths."""
    from pathlib import Path

    bwrite(
        {b'foo': 42, b'bar': {b'sketch': b'parrot', b'foobar': 23}},
        Path(TEMP_DIR, 'beta')
    )

    with open(os.path.join(TEMP_DIR, 'beta'), 'rb') as fp:
        assert fp.read() == b'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee'
