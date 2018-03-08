#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Film


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class ResultHandler(BaseHandler):
    def post(self):
        naslov = self.request.get("naslov_filma")
        reziser = self.request.get("reziser")
        leto_izida = self.request.get("leto_izida")
        slika = self.request.get("slika")
        ocena = self.request.get("ocena")

        shrani = Film(naslov=naslov, reziser=reziser, leto=leto_izida, url_slike=slika, ocena=ocena)
        shrani.put()
        self.redirect_to("seznam")

class SeznamHandler(BaseHandler):
    def get(self):
        seznam = Film.query(Film.izbrisano == False).fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam.html", params=params)

class SeznamPosodobiHandler(BaseHandler):
    def get(self, message_id):
        shrani = Film.get_by_id(int(message_id))

        params = {"shrani": shrani}
        return self.render_template("seznam_posodobi.html", params=params)

    def post(self, message_id):
        shrani = Film.get_by_id(int(message_id))
        shrani.naslov = self.request.get("nov_naslov")
        shrani.reziser = self.request.get("nov_reziser")
        shrani.url_slike = self.request.get("nov_url_slike")
        shrani.ocena = self.request.get("ocena")
        shrani.put()
        return self.redirect_to("seznam")

class SeznamSkrijHandler(BaseHandler):
    def get(self, message_id):
        shrani = Film.get_by_id(int(message_id))

        params = {"shrani": shrani}
        return self.render_template("seznam_skrij.html", params=params)

    def post(self, message_id):
        shrani = Film.get_by_id(int(message_id))
        shrani.izbrisano = True
        shrani.put()
        return self.redirect_to("seznam")

class SkritiSeznamHandler(BaseHandler):
    def get(self):
        seznam = Film.query(Film.izbrisano == True).fetch()
        params = {"seznam": seznam}
        return self.render_template("skriti_seznam.html", params=params)

class SkritiSeznamObnoviHandler(BaseHandler):
    def get(self, film_id):
        zapis = Film.get_by_id(int(film_id))
        params = {"zapis": zapis}
        return self.render_template("obnovi.html", params=params)

    def post(self, film_id):
        zapis = Film.get_by_id(int(film_id))
        zapis.izbrisano = False
        zapis.put()
        return self.redirect_to("skriti_seznam")


class SkritiSeznamIzbrisiHandler(BaseHandler):
    def get(self, film_id):
        zapis = Film.get_by_id(int(film_id))
        params = {"zapis": zapis}
        return self.render_template("dokoncno_izbrisi.html", params=params)

    def post(self, film_id):
        zapis = Film.get_by_id(int(film_id))
        zapis.key.delete()
        return self.redirect_to("skriti_seznam")



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
    webapp2.Route('/seznam', SeznamHandler, name="seznam"),
    webapp2.Route('/seznam/<message_id:\d+>/posodobi', SeznamPosodobiHandler),
    webapp2.Route('/seznam/<message_id:\d+>/izbrisi', SeznamSkrijHandler),
    webapp2.Route('/skriti_seznam', SkritiSeznamHandler, name="skriti_seznam"),
    webapp2.Route('/skriti_seznam/<film_id:\d+>/obnovi', SkritiSeznamObnoviHandler),
    webapp2.Route('/skriti_seznam/<film_id:\d+>/dokoncno_izbrisi', SkritiSeznamIzbrisiHandler),
], debug=True)
