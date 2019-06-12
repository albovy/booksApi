import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

import model.user as usr_mgt
import model.book as book_mgt
import model.like as like_mgt
import model.comment as comment_mgt
from model.appinfo import AppInfo


class BookShowCommentHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            comments = comment_mgt.create_query_all_for_user(usr_info)
            books = list()
            for comment in comments:
                books.append(book_mgt.create_query_isbn(comment.isbn))
            access_link = users.create_logout_url("/")
            likes = like_mgt.create_query_all_for_one_user(usr_info.email)
            like_list = list()
            for like in likes:
                like_list.append(like.isbn)
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
    ('/books/comment', BookShowCommentHandler)
], debug=True)
