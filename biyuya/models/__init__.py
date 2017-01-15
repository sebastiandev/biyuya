from uuid import uuid4
from biyuya import app
from pymongo import MongoClient


class ObjectDict(dict):

    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError("%s doesn't have attribute '%s'" % (self.__class__.__name__, key))

    def __setattr__(self, name, val):
        self[name] = ObjectDict(**val) if type(val) is dict else val


class BaseModel(ObjectDict):

    type = None
    collection_name = None
    db = MongoClient(app.config['DATABASE']['uri'])[app.config['DATABASE']['name']]

    def __init__(self, **kwargs):
        super().__init__(**{
            '_id': kwargs.get('_id', str(uuid4()))
        })

        self.update(kwargs)

    @property
    def id(self):
        return self._id

    @classmethod
    def _build_entity(cls, doc):
        raise NotImplementedError()

    @classmethod
    def collection(cls):
        return cls.db[cls.collection_name]

    @classmethod
    def add(cls, doc):
        cls.collection().insert_one(doc)

    @classmethod
    def upsert(cls, *docs):
        for d in docs:
            cls.collection().replace_one({'_id': d.id}, d, upsert=True)

    @classmethod
    def delete(cls, *doc_ids):
        for did in doc_ids:
            cls.collection().delete_one({'_id': did})

    @classmethod
    def find(cls, condition, **kwargs):
        condition.update({'type': cls.type})

        for d in cls.collection().find(condition, **kwargs):
            yield cls._build_entity(d)

    @classmethod
    def all(cls):
        for d in cls.collection().find({'type': cls.type}):
            yield cls._build_entity(d)

    @classmethod
    def by_attr(cls, attr, value, exact=True, many=True, limit=0):
        if exact or type(value) is not str:
            params = {attr: value}
        else:
            params = {attr: {"$regex": '.*?{}.*?'.format(value), "$options": 'si'}}

        if many:
            for d in cls.find(params, limit=limit):
                yield cls._build_entity(d)
        else:
            yield cls._build_entity(cls.collection().find_one(params))

    @classmethod
    def by_id(cls, id):
        return next(cls.by_attr('_id', id, many=False))
