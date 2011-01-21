#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - mail checker.
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

"""This package implements account checker via email for Unhosted.

"""

__all__ = ['IMailer', 'SimpleMailer', 'MailChecker']

from zope import interface
import unhosted.interfaces

class IMailer(interface.Interface):
    """Interface for Unhosted mailers."""

    def mailto(fromaddr, toaddr, message):
        """Send mail to address."""

class SimpleMailer(object):
    """Mailer via standard smtplib module."""

    interface.implements(unhosted.interfaces.IMailer)

    def __init__(self, server="localhost"):
        """C-tor with given SMTP server."""
        self.server = server

    def mailto(self, fromaddr, toaddr, msg):
        """Send mail to address."""
        msg = ("From: %s\r\nTo: %s\r\nX-Mailer: python-unhosted "
            + "(http://code.google.com/p/python-unhosted)\r\n\r\n%s"
            % (fromaddr, ", ".join(toaddrs), msg))
        import smtplib
        server = smtplib.SMTP(self.server)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

class MailChecker(object):
    """Registration checker via email."""

    interface.implements(unhosted.interfaces.IRegistrationChecker)

    def __init__(self, mailer, fromaddr="no-reply@unhosted-node"):
        """C-tor with given mailer."""
        assert unhosted.interfaces.IMailer.providedBy(mailer)
        self.mailer = mailer
        self.fromaddr = fromaddr

    def check(self, account):
        """Send verification mail."""
        pass # TODO
