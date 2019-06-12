from google.appengine.ext import ndb


class Book(ndb.Model):
    isbn = ndb.IntegerProperty(indexed=True, required=True)
    mainComment = ndb.TextProperty(required=True)
    author = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    publisher = ndb.StringProperty(required=True)
    year = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    user = ndb.StringProperty(required=True)
    img = ndb.StringProperty(required=True)
    likes = ndb.IntegerProperty(required=True)

    def __unicode__(self):
        return "ISBN: " + self.isbn + "First Comment: " + self.mainComment


def create_query_all():
    return Book.query().order(-Book.likes)


def create_query_isbn(isbn):
    intIsbn = int(isbn)
    query = Book.query(Book.isbn == intIsbn).get()
    return query


def can_create(book):
    book_bd = create_query_isbn(book.isbn)
    return book_bd


def create(user):
    toret = Book()
    toret.isbn = 0
    toret.mainComment = ""
    toret.title = ""
    toret.publisher = ""
    toret.year = ""
    toret.description = ""
    toret.author = ""
    toret.img = ""
    toret.user = user.email
    toret.likes = 0

    return toret


@ndb.transactional
def update(book):
    """Updates a section.

        :param book: The book to update.
        :return: The key of the record.
    """
    return book.put()
