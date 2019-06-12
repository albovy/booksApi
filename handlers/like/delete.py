import webapp2
from google.appengine.api import users
import model.user as usr_mgt
import model.like as like_mgt
import model.book as book_mgt


class DeleteLike(webapp2.RequestHandler):
    def post(self, isbn):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            like = like_mgt.create(usr_info)
            like.isbn = int(isbn)
            like_mgt.create_query_delete_one(like)

            self.redirect("/books")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    (r'/book/(\d+)/dislike', DeleteLike),
], debug=True)