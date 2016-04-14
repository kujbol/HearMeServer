from mongoengine import Document, DoesNotExist


class BaseDocument(Document):
    def to_dict(self):
        result = self.to_mongo().to_dict()
        result.pop('_cls', None)
        return result

    @classmethod
    def get_by_id(cls, obj_id):
        try:
            return cls.objects.get(id=obj_id)
        except DoesNotExist:
            return None

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }
