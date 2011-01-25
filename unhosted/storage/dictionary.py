#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - dictionary storage class.
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

"""This package implements IStorage wrapper for dict-like objects for Unhosted.

"""

__all__ = ['DictionaryStorage']

from zope import interface
import unhosted.interfaces

class DictionaryStorage(object):
    """Wrapper around any dict-like object."""

    interface.implements(unhosted.interfaces.IStorage)

    class Account(object):
        """Account for DictionaryStorage."""

        interface.implements(unhosted.interfaces.IAccount)

        def __init__(self, user, node, app):
            self.test = user + node + app # TODO

        def __str__(self):
            return self.test # TODO

    def __init__(self, initial=None):
        """C-tor.

        Second parameter is initial value of dictionary:
        {channel : {key : value}}

        """
        self._dict = initial or {}

    def get(self, account, key):
        """Gets value from storage."""
        channel = str(account)
        return self._dict.get(channel, {}).get(key, (None, None))

    def set(self, account, key, value, signature):
        """Sets value in storage."""
        channel = str(account)
        if channel not in self._dict:
            self._dict[channel] = {}
        self._dict[channel][key] = (value, signature)

    def has(self, account, key):
        """Checks key presence in storage."""
        channel = str(account)
        return channel in self._dict and key in self._dict[channel]

    def account(self, user, node, application, **kwargs):
        """Create an account."""
        return self.Account(user, node, application)

