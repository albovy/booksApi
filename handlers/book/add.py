import os
from symbol import decorator

import webapp2

from google.appengine.api import users, memcache

from webapp2_extras import jinja2

import model.user as usr_mgt
import model.book as book_mgt
from lib import httplib2

from lib.googleapiclient.discovery import build

from lib.oauth2client.contrib import appengine

from model.appinfo import AppInfo

http = httplib2.Http(memcache)

decorator = appengine.oauth2decorator_from_clientsecrets(
    'client_secret.json',
    scope='https://www.googleapis.com/auth/books',
    message="MISSING_CLIENT_SECRETS_MESSAGE")
service = build("books", "v1", http=http)


class AddBook(webapp2.RequestHandler):

    @decorator.oauth_required
    def get(self):

        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:

            access_link = users.create_logout_url("/")
            template_values = {
                "info": AppInfo,
                "access_link": access_link,
                "usr_info": usr_info
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("add_book.html", **template_values))
        else:
            self.redirect("/")

        return

    @decorator.oauth_required
    def post(self):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:

            book = book_mgt.create(usr_info)
            book.isbn = int(self.request.get("isbn", "").strip())
            book.mainComment = self.request.get("mainComment", "").strip()

            request = service.volumes().list(q='1')
            HttpRequest = request
            url = "https://www.googleapis.com/books/v1/volumes?country=US&q=isbn:" + str(
                book.isbn) + "&key=" + AppInfo.KeyBooks
            HttpRequest.uri = url

            response = HttpRequest.execute(http=decorator.http())

            if response['totalItems'] > 0:
                items = response['items'][0]['volumeInfo']
                book.title = items['title']
                book.author = items['authors'][0]
                book.publisher = items['publisher']
                book.year = items['publishedDate'].split("T")[0]
                book.description = items['description']
                book.img = items['imageLinks']['thumbnail']
                valor = book_mgt.can_create(book)
                if valor is None:
                    book_mgt.update(book)
                    self.redirect("/books")
                else:
                    self.redirect("/error?msg=Ya existe ese libro&redirect=/book/add")
            else:
                self.redirect("/error?msg=No existe ese libro&redirect=/book/add")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ("/book/add", AddBook),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
