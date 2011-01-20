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

    _code = None

    def code(self):
        """HTTP code."""
        if self._code is None:
            raise NotImplementedError("HttpStatus child must declare _code field")
        return self._code

class HttpBadRequest(HttpStatus):
    """HTTP 400."""

    _code = 400

class HttpGone(HttpStatus):
    """HTTP 410."""

    _code = 410

class HttpForbidden(HttpStatus):
    """HTTP 403."""

    _code = 403

class HttpInternalServerError(HttpStatus):
    """HTTP 500."""

    _code = 500

class HttpServiceUnavailable(HttpStatus):
    """HTTP 513."""

    _code = 513
