#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - HTTP support.
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

"""This package implements Unhosted HTTP support classes."""

class HttpStatus(StandardError):
    """HTTP status abstraction."""

    _header = None

    def header(self):
        """HTTP header."""
        if self._header is None:
            raise NotImplementedError("HttpStatus child must declare _header field")
        return self._header

class HttpOk(HttpStatus):
    """HTTP 200 OK."""

    def header(self):
        return None

class HttpServiceUnavailable(HttpStatus):
    """HTTP 513."""

    _header = "HTTP/1.1 513 Service Unavailable"

class HttpBadRequest(HttpStatus):
    """HTTP 400."""

    _header = "HTTP/1.1 400 Bad Request"

class HttpGone(HttpStatus):
    """HTTP 410."""

    _header = "HTTP/1.1 410 Gone"

class HttpForbidden(HttpStatus):
    """HTTP 402."""

    _header = "HTTP/1.1 402 Forbidden"

class HttpNotFound(HttpStatus):
    """HTTP 404."""

    _header = "HTTP/1.1 404 Not Found"

class HttpInternalServerError(HttpStatus):
    """HTTP 500."""

    _header = "HTTP/1.1 500 Internal Server Error"

