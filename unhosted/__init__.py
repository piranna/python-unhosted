#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node.
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

"""This package implements Unhosted server-side classes and handlers.

This package exports Unhosted and Storage classes.

"""

__all__ = ['Storage', 'Unhosted']
__version_info__ = ('0', '2', '0')
__version__ = '.'.join(__version_info__)

import zope.interface

class IStorage(zope.interface.Interface):
    """Interface for Unhosted storages."""

    def get(account, key):
        """Gets (value, signature) from storage or None."""

    def set(account, key, value, signature):
        """Sets value and signature in storage."""

    def has(account, key):
        """Checks key presence in storage."""

    def account(userName, userDomain, node, application, **kwargs):
        """Construct an account for further use in storage.

        This call generally doesn't check for existence and correctness.
        This checks are done by some call that uses account.

        Returns IAccount. Real type depends on storage implementation.

        """

class IRegistrationChecker(zope.interface.Interface):
    """Interface for Unhosted account registration checker."""

    def check(account):
        """Start checking process for account.

        Account should implement IAccount.

        """

class IAccount(zope.interface.Interface):
    """Interface for Unhosted account.

    Account instances shouldn't be created directly, use IStorage.account()
    instead.

    """

class Unhosted(object):
    """Class representing Unhosted engine."""

    def __init__(self, storage, registrationChecker):
        """C-tor.

        Argument 'storage' should be of type unhosted.Storage.

        """
        assert IStorage.providedBy(storage)
        self.storage = storage
        assert IRegistrationChecker.providedBy(registrationChecker)
        self.registrationChecker = registrationChecker

        import unhosted.protocol_0_2
        self.protocol_0_2 = unhosted.protocol_0_2.Unhosted_0_2(self)

    def processRequest(self, request):
        """Process RPC request (either json string or dict)."""
        if isinstance(request, str):
            import unhosted.utils
            request = unhosted.utils.jread(request)
        import unhosted.http
        try:
            proto = request["protocol"]
        except KeyError:
            raise unhosted.http.HttpBadRequest("protocol field is obligatory")

        if proto == "UJ/0.2":
            return self.protocol_0_2.process(request)
        else:
            raise unhosted.http.HttpBadRequest("unsupported protocol %s" % proto)
