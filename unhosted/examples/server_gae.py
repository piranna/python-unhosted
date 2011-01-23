#!/usr/bin/python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# if we don't have unhosted installed (example purposes only)...
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))

from unhosted import Unhosted
from unhosted.checker  import void
from unhosted.modules  import keyvalue
from unhosted.platform import gae as platform
from unhosted.storage  import gae as storage


class File(webapp.RequestHandler):
    '''
    Class that somewhat mimics twisted.web.static.File for Google AppEngine

    This class allow to get the content of a file or a directory filesystem.
    '''
    path = "."

    def get(self, path):
        import os
        import stat

        try:
            pathname = os.path.abspath(os.path.join(self.path,path))
            mode = os.stat(pathname)[stat.ST_MODE]
            if stat.S_ISDIR(mode):
                self.response.out.write('<html>')
                self.response.out.write('<head><title>%s</title></head>'%path)
                self.response.out.write('<body><ul>')
                for entry in os.listdir(pathname):
                    self.response.out.write('<li><a href="%s">%s</a></li>'%(path+'/'+entry,entry))
                self.response.out.write('</ul></body></html>')

            elif stat.S_ISREG(mode):
                with open(pathname, 'r') as f:
                    self.response.out.write(f.read())

        except OSError:
            self.error(404)
#            web.ctx.status = '404 Not file %s found'%path


# Connect database and UnHosted interface
db = storage.GaeDB()
uh = Unhosted(db, void.VoidChecker())
uh.registerModule(keyvalue.KeyValue_0_2(), ["KeyValue-0.2"])

# Serve webpages and UnHosted RPC
platform.Unhosted.unhosted = uh

application = webapp.WSGIApplication([('/unhosted', platform.Unhosted),
                                      ('/(.*)',     File)],
                                     debug=True)

# Start server
run_wsgi_app(application)