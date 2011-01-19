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
import unhosted.storage
import unhosted.utils

class UtilsTestCase(unittest.TestCase):

    def test_10_json(self):
        obj = {"1" : 2, "3" : ["a", None, 42], "4" : None, "5" : "6"}
        json = unhosted.utils.jwrite(obj)
        self.failUnlessEqual(unhosted.utils.jread(json), obj)

    def test_20_md5(self):
        testData = {
            ""      : "d41d8cd98f00b204e9800998ecf8427e",
            "test"  : "098f6bcd4621d373cade4e832627b4f6"
        }
        for key, value in testData.iteritems():
            self.failUnlessEqual(value, unhosted.utils.md5(key).hexdigest())