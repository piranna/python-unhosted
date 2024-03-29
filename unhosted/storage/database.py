#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - database storage class.
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

"""This package implements storage in DB-API 2.0 database for Unhosted.

"""

__all__ = ['DatabaseStorage']

from zope import interface
import unhosted.interfaces

def runInteraction(method):
    """Run safe database interaction.

    Calls 'method' argument with specially created cursor and all other
    parameters passed to this method.
    Commits on success, rollbacks on raised exception.
    Propagates any raised exceptions.

    """

    def wrapped(self, *args, **kwargs):
        try:
            result = method(self, cursor=self._db.cursor(), *args, **kwargs)
        except:
            self._db.rollback()
            raise

        self._db.commit()
        return result

    return wrapped


class DatabaseStorage(object):
    """Wrapper storage for any DB-API 2.0 compatible database."""

    interface.implements(unhosted.interfaces.IStorage)

    class Account(object):
        """Account for DatabaseStorage."""

        interface.implements(unhosted.interfaces.IAccount)

        def __init__(self, user, node, app):
            self.test = user + node + app # TODO

        def __str__(self):
            return self.test # TODO

    def __init__(self, database):
        """C-tor.

        Argument 'database' should be any DB-API 2.0 compatible connection.
        You may need to call initializeDB() to create all required tables.

        """

        self._db = database


    @runInteraction
    def initializeDB(self, cursor=None):
        """Initialize database for Unhosted."""
        if not cursor:
            cursor = self._db.cursor()

        cursor.execute(
        """ CREATE TABLE IF NOT EXISTS unhosted
            (
                channel varchar(255),
                path varchar(255),
                value blob

                PRIMARY KEY(channel, path)
            )""")


    def get(self, channel, key, default=None, cursor=None):
        """Gets value from storage."""
        if not cursor:
            cursor = self._db.cursor()

        row = cursor.execute(
        """ SELECT value FROM unhosted
            WHERE channel=? AND key=?
            LIMIT 1
        """,(channel, key)).fetchone()

        if row is None:
            return default
        return row[0]


    @runInteraction
    def set(self, channel, key, value, cursor=None):
        """Sets value in storage."""
        if not cursor:
            cursor = self._db.cursor()

        if self.has(channel, key, cursor):
            cursor.execute(
            """ UPDATE unhosted
                SET value=? channel=? AND key=?
                LIMIT 1
            """,(value, channel, key))
        else:
            cursor.execute(
            """ INSERT INTO unhosted(value, channel, path)
                VALUES(?,?,?)
                LIMIT 1
            """,(value, channel, key))


    def has(self, channel, key, cursor=None):
        """Checks key presence in storage."""
        if not cursor:
            cursor = self._db.cursor()

        row = cursor.execute(
        """ SELECT COUNT(*) FROM unhosted
            WHERE channel=? AND key=?
            LIMIT 1
        """,(channel, key)).fetchone()

        return row[0] > 0


    def account(self, user, node, application, **kwargs):
        """Create an account."""
        return self.Account(user, node, application)
