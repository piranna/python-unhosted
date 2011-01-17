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

"""This package implements Unhosted UJ/0.2."""

import unhosted.http


class KV(object):
    '''
    Key-Value module
    '''
    def __init__(self, processor):
        self._processor = processor

    def GET(self, request):
        """KV.GET"""
        (keyPath,) = self._processor._fetchFields(request, "keyPath")
        acc = self._processor._fetchAccount(request, "subPass")
        value, signature = self._processor.unhosted.storage.get(acc, keyPath)
        return {"value" : value, "PubSign/0.2" : signature}

    def SET(self, request):
        """KV.SET"""
        (keyPath, value, PubSign) = self._processor._fetchFields(request, "keyPath", "value", "PubSign")
        acc = self._processor._fetchAccount(request, "pubPass")
        return self._processor.unhosted.storage.set(acc, keyPath, value, PubSign)


class Unhosted_0_2(object):
    """Unhosted UJ/0.2 implementation."""

    def __init__(self, unhosted):
        """C-tor."""
        self.unhosted = unhosted

        # Modules
        self.modules = {'KV': KV(self)}

    def process(self, request):
        """Process UJ/0.2 request."""
        # Get action
        try:
            action = request["action"]
        except KeyError:
            raise unhosted.http.HttpBadRequest("action field is obligatory")

        try:
            action = str(action).strip()
        except (TypeError, ValueError):
            raise unhosted.http.HttpBadRequest("malformed action: %s" % action)

        if not action:
            raise unhosted.http.HttpBadRequest("empty action field")

        # Get requested method from the action
        try:
            action = action.split(".")
            module = self.modules[action[0]]
            proc = getattr(module, action[1])
        except KeyError:
            raise unhosted.http.HttpBadRequest("module not available: %s" % action[0])
        except AttributeError:
            raise unhosted.http.HttpBadRequest("unsupported action: %s" % action)
        except TypeError:
            raise unhosted.http.HttpInternalServerError("%s is an attribute" % action)

        return proc(request)

    # Protected

    def _fetchAccount(self, request, *otherParams):
        """Check and fetch account from request."""
        try:
            params = (request["emailUser"], request["emailDomain"],
                request["storageNode"], request["app"])
        except KeyError:
            raise unhosted.http.HttpBadRequest("emailUser, emailDomain, storageNode (or HOST), "
                + " app (or REFERRER) required for %s action" % request["action"])
        kwparams = {}
        for other in otherParams:
            try:
                kwparams[other] = request[other]
            except KeyError:
                raise unhosted.http.HttpBadRequest("%s required for %s action"
                    % (other, request["action"]))
        return self.unhosted.storage.account(*params, **kwparams)

    def _fetchFields(self, request, *fields):
        """Checks and fetch fields from request."""
        result = tuple()
        for field in fields:
            try:
                result += (request[field],)
            except KeyError:
                raise unhosted.http.HttpBadRequest("%s required for %s action" %
                    (field, request["action"]))
        return result