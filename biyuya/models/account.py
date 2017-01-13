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
        return next(cls.by_attr('name', name, many=False))

    @classmethod
    def by_currency(cls, currency):
        return cls.by_attr('currency', currency)

