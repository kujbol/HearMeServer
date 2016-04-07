from mongoengine import Document, DoesNotExist


class BaseDocument(Document):
    def to_dict(self):
        return self.to_mongo().to_dict()

    @classmethod
    def get_by_id(cls, obj_id):
        try:
            return cls.objects.get(id=obj_id)
        except DoesNotExist:
            return None

