#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - test for unhosted.
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

from twisted.trial import unittest

import unhosted
import unhosted.dictstorage
import unhosted.utils
import unhosted.modules.keyvalue

class Unhosted_0_2_TestCase(unittest.TestCase):

    def test_10_unhosted_instance(self):
        uh = unhosted.Unhosted(
            unhosted.dictstorage.DictStorage({}),
            unhosted.utils.VoidChecker())

    def test_20_KV_GET_empty(self):
        uh = unhosted.Unhosted(
            unhosted.dictstorage.DictStorage({}),
            unhosted.utils.VoidChecker())
        uh.registerModule(unhosted.modules.keyvalue.KeyValue_0_2(), ["KV"])

        request = {
            "protocol"      : "UJ/0.2",
            "emailUser"     : "testUser",
            "emailDomain"   : "testDomain",
            "storageNode"   : "testNode",
            "app"           : "testApp",
            "action"        : "KV.GET",
            "keyPath"       : "test",
            "subPass"       : "testPassword"
        }

        response = uh.processRequest(request)
        self.failUnlessIsInstance(response, dict)
        self.failUnlessEqual(response["value"], None)
        self.failUnlessEqual(response["PubSign/0.2"], None)

    def test_30_KV_GET_SET(self):
        uh = unhosted.Unhosted(
            unhosted.dictstorage.DictStorage({}),
            unhosted.utils.VoidChecker())
        uh.registerModule(unhosted.modules.keyvalue.KeyValue_0_2(), ["KV"])

        request = {
            "protocol"      : "UJ/0.2",
            "emailUser"     : "testUser",
            "emailDomain"   : "testDomain",
            "storageNode"   : "testNode",
            "app"           : "testApp",
            "action"        : "KV.SET",
            "keyPath"       : "test",
            "pubPass"       : "testPassword",
            "value"         : "testValue",
            "PubSign/0.2"   : "testSign"
        }

        response = uh.processRequest(request)
        self.failUnlessIsInstance(response, dict)
        self.failUnlessEqual(response, {})

        request = {
            "protocol"      : "UJ/0.2",
            "emailUser"     : "testUser",
            "emailDomain"   : "testDomain",
            "storageNode"   : "testNode",
            "app"           : "testApp",
            "action"        : "KV.GET",
            "keyPath"       : "test",
            "subPass"       : "testPassword"
        }

        response = uh.processRequest(request)
        self.failUnlessIsInstance(response, dict)
        self.failUnlessEqual(response["value"], "testValue")
        self.failUnlessEqual(response["PubSign/0.2"], "testSign")
