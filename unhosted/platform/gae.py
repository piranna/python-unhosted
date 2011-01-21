from google.appengine.ext import webapp

from unhosted import Unhosted,utils
from unhosted.checker.void import VoidChecker


class UnhostedRequestHandler(webapp.RequestHandler):
    '''
    Google AppEngine request handler for UnHosted
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Connect database and UnHosted interface
        self.unhosted = Unhosted(GaeDB(), VoidChecker())


    def post(self):
        '''
        Render POST request
        '''
        args = _convertArgs(self.request.args)
        data = self.unhosted.processRequest(args)

#        data = _processDeferreds(data)

#        if :
        data = self._ready(data)
#        else:
#            data = self._error(err)

        self.response.out.write(data)


    def _ready(self, data):
        """Requested data ready."""
        if data:
            if not isinstance(data, str):
                data = utils.jwrite(data)
            self.response.out.write(data + "\n")