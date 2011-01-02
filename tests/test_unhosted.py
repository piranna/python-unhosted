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

class UnhostedTestCase(unittest.TestCase):

    def setUp(self):
        import unhosted

    def tearDown(self):
        pass

    def test_10_storage(self):
        import unhosted
        import unhosted.storage

        # Instance for testing
        storage = unhosted.storage.DictStorage({})

        # Params required
        self.failUnlessRaises(TypeError, storage.get)
        self.failUnlessRaises(TypeError, storage.set)
        self.failUnlessRaises(TypeError, storage.has)

        # Get-set-has
        self.failIf(storage.has("account", "key"))
        storage.set("account", "key", "value")
        self.failUnless(storage.has("account", "key"))
        self.failUnlessEqual(storage.get("account", "key"), "value")
        self.failUnless(storage.has("account", "key"))
        self.failIf(storage.has("account1", "key"))
        self.failIf(storage.has("account", "key1"))
        self.failIf(storage.has("account1", "key1"))

    def test_20_json(self):
        import unhosted.json
        obj = {"1" : 2, "3" : ["a", None, 42], "4" : None, "5" : "6"}
        json = unhosted.json.jwrite(obj)
        self.failUnlessEqual(unhosted.json.jread(json), obj)

    def test_30_unhosted_0_2(self):
        import unhosted
        import unhosted.storage
        uh = unhosted.Unhosted(unhosted.storage.DictStorage({}))
