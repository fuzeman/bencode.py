#!/usr/bin/env python
#
# Copyright (c) 2010 BitTorrent Inc.
#

"""bencode.py - setup script."""

from setuptools import setup, find_packages


setup(
    name="bencode.py",
    version="1.1.0",
    packages=find_packages(),

    author="Dean Gardiner",
    author_email="me@dgardiner.net",
    description="BitTorrent bencode module with Python 3+ compatibility.",
    license="BitTorrent Open Source License",
    keywords="bittorrent bencode bdecode"
)
