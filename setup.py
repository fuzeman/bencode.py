#!/usr/bin/env python
#
# Copyright (c) 2010 BitTorrent Inc.
#

from setuptools import setup, find_packages

setup(
    name="bencode.py",
    version="1.0",
    packages=find_packages(),

    author="Dean Gardiner",
    author_email="me@dgardiner.net",
    description="Fork of the BitTorrent bencode module with Python 3 compatibility.",
    license="BitTorrent Open Source License",
    keywords="bittorrent bencode bdecode"
)
