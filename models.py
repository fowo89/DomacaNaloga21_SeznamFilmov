from google.appengine.ext import ndb


class Film(ndb.Model):
    naslov = ndb.StringProperty()
    reziser = ndb.StringProperty()
    leto = ndb.StringProperty()
    url_slike = ndb.TextProperty()
    ocena = ndb.TextProperty()
    time_date = ndb.DateTimeProperty(auto_now_add=True)
    izbrisano = ndb.BooleanProperty(default=False)
