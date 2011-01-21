from google.appengine.ext import db


class GaeDB(object):
    class unhosted(db.Model):
        channel = db.StringProperty()
        key = db.StringProperty()
        value = db.BlobProperty()

        #PRIMARY KEY(channel, path)


    def initializeDB(self):
        '''
        Initialize database for Unhosted.
        '''
        pass

    def get(self, channel, key, default=None):
        '''
        Gets value from storage.
        '''
        ret = self.has(channel, key)
        return ret.value if ret else default

    def set(self, channel, key, value):
        '''
        Sets value in storage.
        '''
        entity = self.has(channel, key)
        if entity:
            if value == entity.value:
                return
            entity.value = value
        else:
            entity = self.unhosted(channel=channel, key=key, value=value)
        entity.put()

    def has(self, channel, key):
        '''
        Checks key presence in storage.
        '''
        query = self.unhosted.all()
        query.filter('channel =',channel).filter('key =',key)
        return query.get()