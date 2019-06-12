from time import sleep

import webapp2
from google.appengine.api import users
import model.user as usr_mgt
import model.like as like_mgt
import model.book as book_mgt


class AddLike(webapp2.RequestHandler):
    def post(self, isbn):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            like = like_mgt.create(usr_info)
            like.isbn = int(isbn)
            like_mgt.can_be_created(like)
            sleep(2)
            self.redirect("/books")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    (r'/book/(\d+)/like', AddLike),
], debug=True)
