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
    def _collection(cls):
        return cls.db[cls.collection_name]

    @classmethod
    def add(cls, doc):
        cls._collection().insert_one(doc)

    @classmethod
    def upsert(cls, *docs):
        for d in docs:
            cls._collection().replace_one({'_id': d.id}, d, upsert=True)

    @classmethod
    def delete(cls, *docs):
        cls._collection().delete_many(docs)

    @classmethod
    def all(cls):
        for d in cls._collection().find({'type': cls.type}):
            yield cls._build_entity(d)

    @classmethod
    def by_id(cls, id):
        return cls._build_entity(cls._collection().find_one({'_id': id}))
