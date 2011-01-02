#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python library for Unhosted storage node - additional storage classes.
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

"""This package implements some storage classes for Unhosted.

"""

__all__ = ['DatabaseStorage', 'DictStorage']

import unhosted
import zope.interface

class DictStorage(object):
    """Wrapper around any dict-like object."""

    zope.interface.implements(unhosted.IStorage)

    def __init__(self, initial=None):
        """C-tor.

        Second parameter is initial value of dictionary:
        {channel : {key : value}}

        """
        self._dict = initial or {}

    def get(self, channel, key, default=None):
        """Gets value from storage."""
        return self._dict.get(channel, {}).get(key, default)

    def set(self, channel, key, value):
        """Sets value in storage."""
        if not channel in self._dict:
            self._dict[channel] = {}
        self._dict[channel][key] = value

    def has(self, channel, key):
        """Checks key presence in storage."""
        return channel in self._dict and key in self._dict[channel]

class DatabaseStorage(object):
    """Wrapper storage for any DB-API 2.0 compatible database."""

    zope.interface.implements(unhosted.IStorage)

    def __init__(self, database):
        """C-tor.

        Argument 'database' should be any DB-API 2.0 compatible connection.
        You may need to call initializeDB() to create all required tables.

        """
        self._db = database

    def initializeDB(self):
        """Initialize database for Unhosted."""
        self._runInteraction(self.__realInitializeDB)

    def get(self, channel, key, default=None):
        """Gets value from storage."""
        row = self._db.cursor().execute(
            "select value from unhosted where channel=? and key=?",
            (channel, key)
        ).fetchone()

        if row is None:
            return default
        else:
            return row[0]

    def set(self, channel, key, value):
        """Sets value in storage."""
        self._runInteraction(self.__realSet, channel, key, value)

    def has(self, channel, key):
        """Checks key presence in storage."""
        row = self._db.cursor().execute(
            "select count(*) from unhosted where channel=? and key=?",
            (channel, key)
        ).fetchone()
        return row[0] > 0

    # Protected

    def _runInteraction(self, call, *args, **kwargs):
        """Run safe database interaction.

        Calls 'call' argument with specially created cursor and all other
        parameters passed to this method.
        Commits on success, rollbacks on raised exception.
        Propagates any raised exceptions.

        """
        if not callable(call):
            raise TypeError("call argument must be callable")

        cursor = self._db.cursor()
        try:
            result = call(cursor, *args, **kwargs)
        except:
            self._db.rollback()
            raise

        self._db.commit()
        return result

    # Private

    def __realInitializeDB(self, cursor):
        """Initialize database for Unhosted (private method)."""
        cursor.execute("""CREATE TABLE IF NOT EXISTS unhosted (
            channel varchar(255),
            path varchar(255),
            value blob
            PRIMARY KEY (channel, path)
        )""")

    def __realSet(self, cursor, channel, key, value):
        row = cursor.execute("select count(*) from unhosted channel=? and key=?",
            (channel, key))
        if row[0] > 0:
            cursor.execute("update unhosted set value=? channel=? and key=?",
                (value, channel, key))
        else:
            cursor.execute("insert into unhosted (value, channel, path) values (?,?,?)",
                (value, channel, key))

