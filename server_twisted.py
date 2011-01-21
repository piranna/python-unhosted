#!/usr/bin/python
import argparse
import sqlite3

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from unhosted import Unhosted, checker
from unhosted.modules  import keyvalue
from unhosted.platform import tx
from unhosted.storage  import database

# Command line arguments
parser = argparse.ArgumentParser(description='UnHosted node and webpages server.')
parser.add_argument('--database', default=':memory:',
                    help='database where to store UnHosted key-value pairs')
parser.add_argument('--rootdir', default='.',
                    help='root directory of the webserver')
args = parser.parse_args()

# Connect database and UnHosted interface
db = database.DatabaseStorage(sqlite3.connect(args.database))
uh = Unhosted(db, checker.VoidChecker())
uh.registerModule(keyvalue.KeyValue_0_2(), ["KeyValue-0.2"])

# Serve webpages and UnHosted RPC
root = File(args.rootdir)
root.putChild("unhosted", tx.UnhostedResource(uh))

# Start server
reactor.listenTCP(8080, Site(root))
reactor.run()
