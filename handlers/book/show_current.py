import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

import model.user as usr_mgt
import model.book as book_mgt
import model.comment as comment_mgt


from model.appinfo import AppInfo


class BookShowCurrentHandler(webapp2.RequestHandler):
    def get(self, isbn):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)
        comments = comment_mgt.create_query_all_for_one_isbn(isbn)

        if user and usr_info:
            book = book_mgt.create_query_isbn(isbn)
            access_link = users.create_logout_url("/")

            template_values = {
                "info": AppInfo,
                "access_link": access_link,
                "book": book,
                "comments": comments,
                "usr_info": usr_info
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("show_current_book.html", **template_values))


app = webapp2.WSGIApplication([
    (r'/book/(\d+)', BookShowCurrentHandler)
], debug=True)
