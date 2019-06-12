from google.appengine.ext import ndb


class Like(ndb.Model):
    user = ndb.StringProperty(required=True)
    isbn = ndb.IntegerProperty(indexed=True, required=True)


def create(user):
    toret = Like()
    toret.user = user.email
    toret.isbn = 0

    return toret


def create_query_all_for_one_user(email):
    return Like.query(Like.user == email).fetch(projection=[Like.isbn])


def create_query_delete_one(like):
    query = Like.query(Like.user == like.user, Like.isbn == like.isbn)
    if query.count() != 0:
        query = Like.query(Like.user == like.user, Like.isbn == like.isbn).get()
        return query.key.delete()


def can_be_created(like):
    query = Like.query(Like.user == like.user, Like.isbn == like.isbn)
    if query.count() == 0:
        update(like)


def cant_likes(isbn):
    query = Like.query(Like.isbn == isbn).count()

    return query


@ndb.transactional
def update(like):
    """Updates a section.

        :param like: The like to update.
        :return: The key of the record.
    """
    return like.put()
