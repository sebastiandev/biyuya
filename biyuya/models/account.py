from . import BaseModel


class Account(BaseModel):

    type = 'account'
    collection_name = 'expenses'

    def __init__(self, name=None, currency=None, notes=None, **kwargs):
        if 'type' in kwargs:
            kwargs.pop('type')

        super().__init__(**{
            'type': Account.type,
            'name': name,
            'currency': currency,
            'notes': notes
        }, **kwargs)

    @classmethod
    def _build_entity(cls, doc):
        return Account(**doc) if doc else None

    @classmethod
    def by_name(cls, name):
        return cls._build_entity(cls._collection().find_one({'name': name}))

