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

class Unhosted_0_2(object):
    """Unhosted UJ/0.2 implementation."""

    def __init__(self, unhosted):
        """C-tor."""
        self.unhosted = unhosted

    def process(self, request):
        """Process UJ/0.2 request."""
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

        try:
            proc = getattr(self, "_handle_" + action.replace(".", "_"))
        except AttributeError:
            raise unhosted.http.HttpBadRequest("unsupported action: %s" % action)

        assert callable(proc)

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

    def _handle_KV_GET(self, request):
        """KV.GET"""
        (keyPath,) = self._fetchFields(request, "keyPath")
        acc = self._fetchAccount(request, "subPass")
        value, signature = self.unhosted.storage.get(acc, keyPath)
        return {"value" : value, "PubSign/0.2" : signature}
