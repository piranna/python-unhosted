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

        cursor.execute("""CREATE TABLE IF NOT EXISTS unhosted (
            channel varchar(255),
            path varchar(255),
            value blob
            PRIMARY KEY (channel, path)
        )""")

    def get(self, channel, key, default=None, cursor=None):
        """Gets value from storage."""
        if not cursor:
            cursor = self._db.cursor()

        row = cursor.execute("select value from unhosted where channel=? and key=?",
                             (channel, key)
        ).fetchone()

        if row is None:
            return default
        return row[0]

    @runInteraction
    def set(self, channel, key, value, cursor=None):
        """Sets value in storage."""
        if not cursor:
            cursor = self._db.cursor()

        row = cursor.execute("select count(*) from unhosted channel=? and key=?",
                             (channel, key))
        if row[0] > 0:
            cursor.execute("update unhosted set value=? channel=? and key=?",
                           (value, channel, key))
        else:
            cursor.execute("insert into unhosted (value, channel, path) values (?,?,?)",
                           (value, channel, key))

    def has(self, channel, key, cursor=None):
        """Checks key presence in storage."""
        if not cursor:
            cursor = self._db.cursor()

        row = cursor.execute("select count(*) from unhosted where channel=? and key=?",
                             (channel, key)
        ).fetchone()
        return row[0] > 0
