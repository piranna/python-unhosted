#!/usr/bin/python
import argparse
import sqlite3

import web

from unhosted import Unhosted
from unhosted.checker  import void
from unhosted.modules  import keyvalue
from unhosted.platform import webpy
from unhosted.storage  import database


# Command line arguments
parser = argparse.ArgumentParser(description='UnHosted node and webpages server.')
parser.add_argument('--database', default=':memory:',
                    help='database where to store UnHosted key-value pairs')
parser.add_argument('--rootdir', default='.',
                    help='root directory of the webserver')
args = parser.parse_args()


class File:
    '''
    Class that somewhat mimics twisted.web.static.File for web.py

    This class allow to get the content of a file or a directory filesystem.
    '''
    path = "."

    def GET(self, path):
        from os.path import abspath,join

        with open(abspath(join(self.path,path)), 'r') as f:
            return f.read()


# Connect database and UnHosted interface
db = database.DatabaseStorage(sqlite3.connect(args.database))
uh = Unhosted(db, void.VoidChecker())
uh.registerModule(keyvalue.KeyValue_0_2(), ["KeyValue-0.2"])

# Serve webpages and UnHosted RPC
File.path = args.rootdir
webpy.Unhosted.unhosted = uh

app = web.application(('/unhosted','webpy.Unhosted',
                       '/(.*)','File'),
                       globals())

# Start server
app.run()