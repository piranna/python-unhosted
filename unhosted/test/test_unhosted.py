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
import unhosted.storage.dictionary
import unhosted.checker.void
import unhosted.modules.keyvalue

class Unhosted_0_2_TestCase(unittest.TestCase):

    def test_10_unhosted_instance(self):
        uh = unhosted.Unhosted(
            unhosted.storage.dictionary.DictionaryStorage({}),
            unhosted.checker.void.VoidChecker())

    def test_20_KV_GET_empty(self):
        uh = unhosted.Unhosted(
            unhosted.storage.dictionary.DictionaryStorage({}),
            unhosted.checker.void.VoidChecker())
        unhosted.modules.keyvalue.KeyValue_0_2().install(uh)

        request = {
            "protocol"      : unhosted.Unhosted.baseProtocol + "KeyValue-0.2",
            "storageNode"   : "testNode",
            "app"           : "testApp",
            "command"       : {
                "method"    : "GET",
                "user"      : "testUser",
                "keyHash"   : "testKey"
            }
        }

        response = uh.processRequest(request)
        self.failUnlessIsInstance(response, dict)
        self.failUnlessEqual(response["value"], None)
        self.failUnlessEqual(response["PubSign"], None)

    def test_30_KV_GET_SET(self):
        uh = unhosted.Unhosted(
            unhosted.storage.dictionary.DictionaryStorage({}),
            unhosted.checker.void.VoidChecker())
        unhosted.modules.keyvalue.KeyValue_0_2().install(uh)

        request = {
            "protocol"      : unhosted.Unhosted.baseProtocol + "KeyValue-0.2",
            "storageNode"   : "testNode",
            "app"           : "testApp",
            "command"       : {
                "method"    : "SET",
                "user"      : "testUser",
                "keyHash"   : "testKey",
                "value"     : "testValue"
            },
            "password"      : "testPassword",
            "pubSign"       : "testSign"
        }

        response = uh.processRequest(request)
        self.failUnlessIsInstance(response, dict)
        self.failUnlessEqual(response, {})

        request = {
            "protocol"      : unhosted.Unhosted.baseProtocol + "KeyValue-0.2",
            "storageNode"   : "testNode",
            "app"           : "testApp",
            "command"       : {
                "method"    : "GET",
                "user"      : "testUser",
                "keyHash"   : "testKey"
            }
        }

        response = uh.processRequest(request)
        self.failUnlessIsInstance(response, dict)
        self.failUnlessEqual(response["value"], "testValue")
        self.failUnlessEqual(response["PubSign"], "testSign")
