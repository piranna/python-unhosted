#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - JSON implementation.
# Copyright 2010 Dmitrij "Divius" Tantsur <divius.inside@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

"""This package contains some utils for Unhosted."""

def _detectJSON():
    """Determine what JSON module we have."""
    # Try use anyjson to detect the fastest module
    try:
        import anyjson
        return anyjson.deserialize, anyjson.serialize, ValueError, TypeError
    except (ImportError, AttributeError):
        pass

    # Module json is available in standard library
    try:
        import json
        return json.loads, json.dumps, ValueError, TypeError
    except (ImportError, AttributeError):
        pass

    # Now try minjson from python-json package (available for Python 2.4)
    try:
        import minjson
        return minjson.read, minjson.write, minjson.ReadException, minjson.WriteException
    except (ImportError, AttributeError):
        raise ImportError("No JSON modules are present (currently supported: " +
            + "anyjson, json (python >= 2.6), minjson")

jread, jwrite, JReadError, JWriteError = _detectJSON()

def _detectMD5():
    """Detect md5 implementation for current version of Python."""
    try:
        from hashlib import md5
    except ImportError:
        from md5 import new as md5
    return md5

md5 = _detectMD5()