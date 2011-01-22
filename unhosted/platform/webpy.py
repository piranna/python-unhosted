import web

import unhosted.utils

from . import _convertArgs


class Unhosted:
    '''
    web.py class for UnHosted
    '''
    unhosted = None


    def POST(self):
        '''
        Render POST request
        '''
        args = _convertArgs(web.input())

        try:
            data = self.unhosted.processRequest(args)
        except:
            data = self._error(err)
        else:
            data = self._ready(data)

        if data:
            return data + "\n"


    # Protected

    def _ready(self, data):
        '''
        Requested data ready
        '''
        if data and not isinstance(data, str):
            return utils.jwrite(data)