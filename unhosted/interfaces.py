#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - interfaces.
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

"""This package implements account checker via email for Unhosted.

"""

__all__ = ['IStorage', 'IRegistrationChecker', 'IAccount', 'IModule']

from zope import interface

class IStorage(interface.Interface):
    """Interface for Unhosted storages."""

    def get(account, key):
        """Gets (value, signature) from storage or None."""

    def set(account, key, value, signature):
        """Sets value and signature in storage."""

    def has(account, key):
        """Checks key presence in storage."""

    def account(user, node, application, **kwargs):
        """Construct an account for further use in storage.

        This call generally doesn't check for existence and correctness.
        This checks are done by some call that uses account.

        Returns IAccount. Real type depends on storage implementation.

        """

class IRegistrationChecker(interface.Interface):
    """Interface for Unhosted account registration checker."""

    def check(account):
        """Start checking process for account.

        Account should implement IAccount.

        """

class IAccount(interface.Interface):
    """Interface for Unhosted account.

    Account instances shouldn't be created directly, use IStorage.account()
    instead.

    """

class IModule(interface.Interface):
    """Interface for Unhosted module."""

    def initialize(unhosted):
        """Initialize module for given unhosted instance."""

    def processCommand(storageNode, app, command):
        """Process single command for this module.

        Can raise various exceptions from unhosted.http.
        Any exceptions that are not derived from unhosted.http.HttpStatus
        will be converted by calling code into unhosted.http.HttpInternalServerError.

        """
