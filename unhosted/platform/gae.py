from google.appengine.ext import webapp

import unhosted.utils

from . import _convertArgs


class Unhosted(webapp.RequestHandler):
    '''
    Google AppEngine request handler for UnHosted
    '''
    unhosted = None


    def post(self):
        '''
        Render POST request
        '''
        args = _convertArgs(self.request.args)

        try:
            data = self.unhosted.processRequest(args)
        except:
            data = self._error(err)
        else:
            data = self._ready(data)

        if data:
            self.response.out.write(data + "\n")


    # Protected


    def _ready(self, data):
        '''
        Requested data ready
        '''
        if data and not isinstance(data, str):
            return utils.jwrite(data)