import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

import model.user as usr_mgt
import model.book as book_mgt
import model.like as like_mgt
from model.appinfo import AppInfo


class BookShowAllHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            books = book_mgt.create_query_all()
            access_link = users.create_logout_url("/")
            likes = like_mgt.create_query_all_for_one_user(usr_info.email)
            like_list = list(likes)
            for like in likes:
                like_list.append(like.isbn)

            for book in books:
                cant_likes = like_mgt.cant_likes(book.isbn)
                if cant_likes != book.likes:
                    book.likes = cant_likes
                    book_mgt.update(book)

            template_values = {
                "info": AppInfo,
                "access_link": access_link,
                "books": books,
                "usr_info": usr_info,
                "likes": like_list
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("books.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/books', BookShowAllHandler)
], debug=True)
