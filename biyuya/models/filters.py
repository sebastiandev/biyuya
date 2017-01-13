

class AttributeFilter(object):

    @classmethod
    def condition(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def apply(cls, model, *args, **kwargs):
        return model.collection().find(cls.condition(*args, **kwargs), limit=kwargs.get('limit', 0))


class DateRangeFilter(AttributeFilter):

    @classmethod
    def condition(cls, from_date, to_date, **kwargs):
        return {'date': {"$gte": from_date, "$lte": to_date}}


class AccountFilter(AttributeFilter):

    @classmethod
    def condition(cls, account_name):
        return {
            'account': {
                "$regex": '.*?{}.*?'.format(account_name),
                "$options": 'si'
            }
        }


class TagFilter(AttributeFilter):

    @classmethod
    def condition(cls, *tags, **kwargs):
        return {
            'tags': {
                "$elemMatch": {
                    "$regex": ".*?{}.*?".format('|'.join(tags)),
                    "$options": "si"
                }
            }
        }

