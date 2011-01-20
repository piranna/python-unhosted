#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - UJ/0.2 implementation.
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

import zope.interface

import unhosted
import unhosted.http

class KeyValue_0_2(object):
    """KeyValue-0.2 module."""

    zope.interface.implements(unhosted.IModule)

    def initialize(self, unhosted):
        """Initialize module for given unhosted instance."""
        self.unhosted = unhosted

    def processRequest(self, request):
        """Process request for this module."""

    def GET(self, request):
        """KV.GET"""
        (keyPath,) = self.unhosted.fetchFields(request, "keyPath")
        acc = self.unhosted.fetchAccount(request, "subPass")
        value, signature = self.unhosted.storage.get(acc, keyPath)
        return {"value" : value, "PubSign/0.2" : signature}

    def SET(self, request):
        """KV.SET"""
        (keyPath, value, PubSign) = self.unhosted.fetchFields(request, "keyPath", "value", "PubSign/0.2")
        acc = self.unhosted.fetchAccount(request, "pubPass")
        self.unhosted.storage.set(acc, keyPath, value, PubSign)
        return {}
