#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node.
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

"""This package implements Unhosted server-side classes and handlers.

This package exports Unhosted and Storage classes.

"""

__all__ = ['Storage', 'Unhosted']
__version_info__ = ('0', '2', '0')
__version__ = '.'.join(__version_info__)

class Unhosted(object):
    """Class representing Unhosted engine."""

    def __init__(self, storage, registrationChecker):
        """C-tor.

        Argument 'storage' should be of type unhosted.Storage.

        """
        from unhosted import interfaces
        if not interfaces.IStorage.providedBy(storage):
            raise TypeError("storage must provide IStorage")
        if not interfaces.IRegistrationChecker.providedBy(registrationChecker):
            raise TypeError("registrationChecker must provide IRegistrationChecker")

        self.storage = storage
        self.registrationChecker = registrationChecker
        self.modules = {}

    def registerModule(self, module, names):
        """Register module instance for given module names."""
        from unhosted import interfaces
        if not interfaces.IModule.providedBy(module):
            raise TypeError("module must provide IModule")
        if not isinstance(names, list):
            raise TypeError("names must be a list of strings")

        for name in names:
            if not isinstance(name, str):
                raise TypeError("names must be a list of strings")
            self.modules[name] = module
        module.initialize(self)

    def processRequest(self, request):
        """Process RPC request (either json string or dict)."""
        if isinstance(request, str):
            import unhosted.utils
            request = unhosted.utils.jread(request)
        import unhosted.http
        try:
            proto = request["protocol"]
        except KeyError:
            raise unhosted.http.HttpBadRequest("protocol field is obligatory")

        if proto == "UJ/0.2":
            return self.process_0_2(request)
        else:
            raise unhosted.http.HttpBadRequest("unsupported protocol %s" % proto)

    def process_0_2(self, request):
        """Process UJ/0.2 request."""
        import unhosted.http
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
            moduleName, procName = action.split(".")
        except ValueError:
            raise unhosted.http.HttpBadRequest("malformed action string: %s" % action)

        try:
            proc = getattr(self.modules[moduleName], procName)
        except KeyError:
            raise unhosted.http.HttpBadRequest("module not available: %s" % moduleName)
        except AttributeError:
            raise unhosted.http.HttpBadRequest("unsupported action: %s" % procName)

        if not callable(proc):
            raise unhosted.http.HttpInternalServerError("%s is an attribute" % action)

        return proc(request)

    def fetchAccount(self, request, *otherParams):
        """Check and fetch account from request."""
        import unhosted.http
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
        return self.storage.account(*params, **kwparams)

    def fetchFields(self, request, *fields):
        """Checks and fetch fields from request."""
        import unhosted.http
        result = tuple()
        for field in fields:
            try:
                result += (request[field],)
            except KeyError:
                raise unhosted.http.HttpBadRequest("%s required for %s action" %
                    (field, request["action"]))
        return result

