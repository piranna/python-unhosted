#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - Twisted support classes.
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

"""This package implements Twisted support for Unhosted.

"""

__all__ = ['UnhostedResource']

from twisted.web import resource, server
from twisted.internet import defer

import unhosted.http
import unhosted.utils

def _processDeferreds(data):
    def _doProcessOneDeferred(value, data, key):
        data[key] = value

    deferlist = []
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], defer.Deferred):
                data[key].addCallback(_doProcessOneDeferred, data, key)
                deferlist.append(data[key])
        return defer.DeferredList(deferlist)
    else:
        return defer.maybeDeferred(data)

class UnhostedResource(resource.Resource):
    """TwistedWeb resource for Unhosted."""

    isLeaf = True

    def __init__(self, unhosted):
        """C-tor."""
        self.unhosted = unhosted

    def render_POST(self, request):
        """Render POST request."""
        request._unhosted_canceled = False
        request._unhosted_d = defer.maybeDeferred(
            self.unhosted.processRequest, request.content.read(),
            request.getRequestHostname(), request.getHeader("referer"))
        request._unhosted_d.addCallback(_processDeferreds)
        request._unhosted_d.addCallback(self._ready, request)
        request._unhosted_d.addErrback(self._error, request)
        request.notifyFinish().addErrback(self._fail, request)
        return server.NOT_DONE_YET

    # Protected

    def _ready(self, data, request):
        """Requested data ready."""
        if data is not None and not isinstance(data, str):
            data = unhosted.utils.jwrite(data)

        request.setResponseCode(200, "OK")
        if data is not None:
            request.write(data + "\n")
        request.finish()

    def _error(self, err, request):
        """Error while requesting data."""
        if request._unhosted_canceled:
            return

        if isinstance(err.value, unhosted.http.HttpStatus):
            request.setResponseCode(err.value.code(), err.getErrorMessage())
        else:
            request.setResponseCode(unhosted.http.HttpInternalServerError._code,
                "Unknown exception: " + err.getErrorMessage())

        request.write(err.getErrorMessage() + "\n")
        request.finish()

    def _fail(self, err, request):
        """Client-side error."""
        request._unhosted_canceled = True
        if request._unhosted_d:
            request._unhosted_d.cancel()
