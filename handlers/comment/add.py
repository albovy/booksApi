from time import sleep

import webapp2
from google.appengine.api import users
import model.user as usr_mgt

import model.comment as comment_mgt


class AddComment(webapp2.RequestHandler):
    def post(self, isbn):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            comment = comment_mgt.create(usr_info)
            comment.isbn = int(isbn)
            comment.comment = self.request.get("comment", "").strip()

            comment_mgt.update(comment)
            sleep(1)
            self.redirect("/book/" + isbn)
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    (r'/book/(\d+)/comment', AddComment),
], debug=True)
