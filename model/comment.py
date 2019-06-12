from google.appengine.ext import ndb



class Comment(ndb.Model):
    user = ndb.StringProperty(required=True)
    comment = ndb.TextProperty(required=True)
    isbn = ndb.IntegerProperty(indexed=True, required=True)


def create_query_all_for_one_isbn(isbn):
    return Comment.query(Comment.isbn == int(isbn))


def create_query_all_for_user(user):
    return Comment.query(Comment.user == user.email)


def create(user):
    toret = Comment()
    toret.isbn = 0
    toret.comment = ""
    toret.user = user.email
    return toret


@ndb.transactional
def update(comment):
    """Updates a section.

        :param comment: The comment to update.
        :return: The key of the record.
    """
    return comment.put()

