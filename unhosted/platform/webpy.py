import web

from . import ConvertArgs
from unhosted import http,utils


class Unhosted:
    """web.py class for UnHosted"""
    unhosted = None


    def POST(self):
        """Render POST request"""
        args = ConvertArgs(web.input())

        try:
            data = self.unhosted.processRequest(args)

        except http.HttpBadRequest, e:
            data = self._error(e)

        else:
            data = self._ready(data)

        if data:
            return data + "\n"


    # Protected

    def _error(self, err):
        """Error while requesting data."""
        if isinstance(err, http.HttpStatus):
            web.ctx.status = err.code()
        else:
            web.ctx.status = http.HttpInternalServerError._code+' '+"Unknown exception:"

        web.ctx.status += ' '+str(err)
        return str(err)


    def _ready(self, data):
        """Requested data ready"""
        if data and not isinstance(data, str):
            return utils.jwrite(data)