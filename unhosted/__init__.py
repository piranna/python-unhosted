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

__all__ = ['Unhosted']
__version_info__ = ('0', '2', '0')
__version__ = '.'.join(__version_info__)

import unhosted.http


class Unhosted(object):
    """Class representing Unhosted engine."""

    baseProtocol = "UJJP/0.2;"

    def __init__(self, storage, registrationChecker):
        """C-tor.

        Argument 'storage' should be of type unhosted.Storage.

        """
        # Check if storage and registrationChecker are both of the correct types
        from unhosted import interfaces
        if not interfaces.IStorage.providedBy(storage):
            raise TypeError("storage must provide IStorage")
        if not interfaces.IRegistrationChecker.providedBy(registrationChecker):
            raise TypeError("registrationChecker must provide IRegistrationChecker")

        # Set values
        self.storage = storage
        self.registrationChecker = registrationChecker
        self.modules = {}


    def registerModule(self, module, names):
        """Register module instance for given module names."""
        # Check if 'module' is a module
        from unhosted import interfaces
        if not interfaces.IModule.providedBy(module):
            raise TypeError("module must provide IModule")

        # Register module both is a string or a list of strings
        def priv_registerModule(name):
            if not isinstance(name, str):
                raise TypeError("names must be a string or a list of strings")
            self.modules[name] = module

        if isinstance(names,list):
            for name in names:
                priv_registerModule(name)
        else:
            priv_registerModule(names)

        # Initialize module
        module.initialize(self)

    def processRequest(self, request, node=None, app=None):
        """Process RPC request (either json string or dict)."""
        # Get UnHosted JSON request from HTTP request
        if isinstance(request, basestring):
            import unhosted.utils
            try:
                request = unhosted.utils.jread(request)
            except unhosted.utils.JReadError:
                raise unhosted.http.HttpBadRequest("cannot parse request")

        # Check for protocol and command parameters
        try:
            proto, command = request["protocol"], request["command"]
        except KeyError:
            raise unhosted.http.HttpBadRequest(
                "the following fields are obligatory: protocol, command")

        if not proto.startswith(self.baseProtocol):
            raise unhosted.http.HttpBadRequest("unsupported protocol %s" % proto)

        proto = proto[len(self.baseProtocol):]

        # Check if module is supported by the system
        try:
            module = self.modules[proto]
        except KeyError:
            raise unhosted.http.HttpBadRequest("unsupported module %s" % proto)

        # Get command field
        if isinstance(command, basestring):
            import unhosted.utils
            try:
                command = unhosted.utils.jread(command)
            except unhosted.utils.JReadError:
                raise unhosted.http.HttpBadRequest("cannot parse command field")

        if node is not None:
            request["storageNode"] = node
        if app is not None:
            request["app"] = app

        # Process command
        return module.processCommand(request, command)