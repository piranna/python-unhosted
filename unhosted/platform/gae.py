from google.appengine.ext import webapp

from . import _convertArgs
from .. import http,utils


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

        except http.HttpBadRequest, e:
            data = self._error(e)

        else:
            data = self._ready(data)

        if data:
            self.response.out.write(data + "\n")


    # Protected

    def _error(self, err):
        '''
        Error while requesting data.
        '''
        if isinstance(err, http.HttpStatus):
            web.ctx.status = err.code()
        else:
            web.ctx.status = http.HttpInternalServerError._code+' '+"Unknown exception:"

        web.ctx.status += ' '+str(err)
        return str(err)


    def _ready(self, data):
        '''
        Requested data ready
        '''
        if data and not isinstance(data, str):
            return utils.jwrite(data)