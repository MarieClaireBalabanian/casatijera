#!/usr/bin/env python

import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import HTTPError


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

import smtplib
class ContactHandler( tornado.web.RequestHandler):
    def get(self, thankyou=False, error=None, seeds=None):
        seeds = seeds or {'name':'', 'contact':'', 'message':''}
        self.render("contact.html", thankyou=thankyou, error=error, **seeds)

    def post(self):
        name = self.get_argument('name', '')
        contact = self.get_argument('contact', '')
        message = self.get_argument('message', '')

        if not ( name and contact and message ):
            seeds = {'name':name, 'contact':contact, 'message':message}
            return self.get( error = 'Please complete all three fields', seeds=seeds) 

        else:
            self.mailpeople( message, contact, name)
            return self.get( thankyou=True)
         

    def mailpeople(self, msg, contact, name):
    
        headers = 'From: mailer@casatijera.com\nSubject: Incoming Message\n\n'
        email = """%s
        message:\n%s\n\n
        name:\n%s\n
        contact info:\n%s\n----""" % ( headers, msg, name, contact)

        try:
            m = smtplib.SMTP('localhost')
    
            recips = ['test@pearachute.com', 'test@nolimyn.com',
                            'info@casatijera.com', 'elizabeth@casatijera.com']
            for recip in recips:
                m.sendmail( 'contactform@casatijera.com', recip, email)
            m.quit()
        except:
            open('mailfail.log', 'a').write(email)
    

class TourHandler(tornado.web.RequestHandler):
    def get(self, page):
        try:
            page = int( page)
        except:
            page = 1

        prevlink = page-1 if page > 1 else False
        nextlink = page+1 if page < 8 else False

        self.render("%d.html"%page, prevlink=prevlink, nextlink=nextlink)

from random  import shuffle
class SchoolHandler(tornado.web.RequestHandler):
    def get( self):
        imgs = os.listdir( "static/school/")
        shuffle( imgs)
        self.render('school.html', imgs=imgs[:13])


class App( tornado.web.Application):
    def __init__(self):
        here = os.path.dirname(__file__)
        _settings = dict(
            login_url="/login",
            template_path= os.path.join( here, "templates"),
            static_path=os.path.join( here, "static"),
            xsrf_cookies= False,
            debug = True,
        )

    
        handlers = [
            (r"/", HomeHandler),
            (r"/contact/?", ContactHandler),
            (r"/school/?", SchoolHandler),
            (r"/?tour/(.+)/?", TourHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **_settings)
    

def main():
    import sys
    import os.path
    from tornado.options import define, options

    define("port", default=8005, help="run on the given port", type=int)
    define("runtests", default=False, help="run tests", type=bool)
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer( App() )
    http_server.listen(options.port)
    print 'Printing on port %d'%options.port
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

