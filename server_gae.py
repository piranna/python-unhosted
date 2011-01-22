#!/usr/bin/python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from unhosted import Unhosted
from unhosted.checker  import void
from unhosted.modules  import keyvalue
from unhosted.platform import gae
from unhosted.storage  import gae


class File(webapp.RequestHandler):
    '''
    Class that somewhat mimics twisted.web.static.File for web.py

    This class allow to get the content of a file or a directory filesystem.
    '''
    path = "."

    def get(self, path):
        from os.path import abspath,join

        with open(abspath(join(self.path,path)), 'r') as f:
            return f.read()


# Connect database and UnHosted interface
db = gae.GaeDB()
uh = Unhosted(db, VoidChecker())
uh.registerModule(keyvalue.KeyValue_0_2(), ["KeyValue-0.2"])

# Serve webpages and UnHosted RPC
File.path = args.rootdir
gae.Unhosted.unhosted = uh

application = webapp.WSGIApplication([('/unhosted', gae.Unhosted),
                                      ('/(.*)',     Main)],
                                     debug=True)

# Start server
run_wsgi_app(application)