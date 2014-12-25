#!/usr/bin/env python
#
#     Copyright (C) 2015 Matej Ramuta, DNAclassroom
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
from google.appengine.api import mail
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               extensions=['jinja2.ext.autoescape'],
                               autoescape=False)


class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        t = jinja_env.get_template(view_filename)
        self.write(t.render(params))


class MainHandler(Handler):
    def get(self):
        self.render_template('coming_soon.html')


class PathsHandler(Handler):
    def get(self):
        self.render_template('paths.html')


class ContactHandler(Handler):
    def post(self):
        email = self.request.get("email")
        hidden = self.request.get("hidden")
        if hidden:
            return self.render_template("coming_soon.html")

        if email:
            contact_form(email=email)
            params = {"error": "Thank you for subscribing! We'll let you know when we launch."}
        else:
            params = {"error": "Please enter you email. We'll let you know when we launch."}

        self.render_template('coming_soon.html', params)


def contact_form(email):
    message_body = '''
		New email from DNAclassroom.com!
		New subscriber:
		Email: {0}
	'''.format(email.encode('utf-8'))

    html_message_body = '''
		<p>New email from DNAclassroom.com!</p>
		<p>New subscriber:</p>
		<p>Email: {0}</p>
	'''.format(email.encode('utf-8'))

    message = mail.EmailMessage(sender="DNAclassroom <matt@ramuta.me>",
                                to="matej.ramuta@gmail.com",
                                subject="Novo sporocilo na DNAclassroom",
                                body=message_body,
                                html=html_message_body)
    message.send()


app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/paths', PathsHandler),
                                  ('/contact', ContactHandler)
                              ], debug=True)
