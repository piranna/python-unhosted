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

import zope.interface
import unhosted

def _detectJSON():
    """Determine what JSON module we have."""
    try:
        # Try use anyjson
        import anyjson
        return anyjson.deserialize, anyjson.serialize
    except (ImportError, AttributeError):
        pass

    # Module json is available in standard library
    try:
        # Try use anyjson
        import json
        return json.loads, json.dumps
    except (ImportError, AttributeError):
        pass

    # Now try minjson from python-json package (available for Python 2.4)
    try:
        import minjson
    except ImportError:
        raise ImportError("No JSON modules are present (currently supported: " +
            + "anyjson, json, minjson")

    try:
        return json.read, json.write
    except AttributeError:
        raise ImportError("No JSON modules are present (currently supported: " +
            + "anyjson, json, minjson")

jread, jwrite = _detectJSON()

def _detectMD5():
    """Detect md5 implementation for current version of Python."""
    try:
        from hashlib import md5
    except ImportError:
        from md5 import new as md5
    return md5

md5 = _detectMD5()

class VoidChecker(object):
    """Registration checker that always succeeds."""

    zope.interface.implements(unhosted.IRegistrationChecker)

    def check(account):
        """Mark account as checked."""
        pass # TODO
