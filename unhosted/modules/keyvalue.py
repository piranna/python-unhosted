#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - KeyValue-0.2 implementation.
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

"""This package implements KeyValue module."""

from zope import interface

import unhosted.interfaces
import unhosted.http

from . import BaseModule

class KeyValue_0_2(BaseModule):
    """KeyValue-0.2 module."""

    interface.implements(unhosted.interfaces.IModule)

    names = ["KeyValue-0.2"]

    def initialize(self, unhosted):
        """Initialize module for given unhosted instance."""
        self.unhosted = unhosted
        self.methods = {
            "GET"   : self._get,
            "SET"   : self._set
        }

    def processCommand(self, request, command):
        """Process single command for this module."""
        try:
            method = command["method"]
        except KeyError:
            raise unhosted.http.HttpBadRequest(
                "method field is obligatory for KeyValue-0.2")

        try:
            method = self.methods[method]
        except KeyError:
            raise unhosted.http.HttpBadRequest(
                "unsupported method for KeyValue-0.2: %s" % method)

        return method(request, command)

    def _get(self, request, command):
        """GET."""
        try:
            key, user, node, app = \
                command["keyHash"], command["user"], \
                request["storageNode"], request["app"]
        except KeyError:
            raise
            raise unhosted.http.HttpBadRequest(
                "the following fields are obligatory for KeyValue-0.2 GET: "
                "command.keyHash, command.user, storageNode, app")

        acc = self.unhosted.storage.account(user, node, app)
        value, signature = self.unhosted.storage.get(acc, key)
        return {"value" : value, "PubSign" : signature}

    def _set(self, request, command):
        """SET."""
        try:
            key, user, value, node, app, password, pubSign = \
                command["keyHash"], command["user"], command["value"], \
                request["storageNode"], request["app"], \
                request["password"], request["pubSign"]
        except KeyError:
            raise
            raise unhosted.http.HttpBadRequest(
                "the following fields are obligatory for KeyValue-0.2 SET: "
                "command.keyHash, command.user, storageNode, app, password, "
                "command.value, pubSign")

        acc = self.unhosted.storage.account(user, node, app, password=password)
        self.unhosted.storage.set(acc, key, value, pubSign)
        return {}
