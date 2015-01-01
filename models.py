from google.appengine.ext import ndb


class Resource(ndb.Model):
    title = ndb.StringProperty()
    resource_type = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)  # add as list tags=['programming', 'biology']
    author = ndb.StringProperty()  # author of the resource
    description = ndb.TextProperty()
    added_by = ndb.StringProperty()  # user who added the resource (email)
    added_ts = ndb.DateTimeProperty(auto_now_add=True)  # added timestamp
    rating = ndb.StringProperty()
    level = ndb.StringProperty()  # for beginners or advanced

    @property
    def get_id(self):
        return self.key().id

    @classmethod
    def create(cls, title, resource_type, tags, author, description, added_by, rating, level):
        resource = cls(title=title,
                       resource_type=resource_type,
                       tags=tags,
                       author=author,
                       description=description,
                       added_by=added_by,
                       rating=rating,
                       level=level)
        resource.put()