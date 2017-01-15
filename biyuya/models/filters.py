import datetime
import arrow


def arrow_datetime(value, name):
    try:
        value = arrow.get(value).datetime
    except Exception as e:
        raise ValueError(e)

    return value


class BaseFilter(object):
    # TODO: Move this class to be part of API FiltrableResource
    #       Leaving implementation to be defined by base class

    name = None
    value_type = None
    allow_multiple = None

    @classmethod
    def condition(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def apply(cls, model, *args, **kwargs):
        return model.find(cls.condition(*args, **kwargs), limit=kwargs.get('limit', 0))


class DateFilter(BaseFilter):

    name = 'date'
    value_type = arrow_datetime
    allow_multiple = False

    @classmethod
    def condition(cls, date_value, **kwargs):
        return {'date': date_value}


class DateRangeFilter(BaseFilter):

    name = 'date_range'
    value_type = arrow_datetime
    allow_multiple = True

    @classmethod
    def condition(cls, from_date, to_date, **kwargs):
        return {'date': {"$gte": from_date, "$lte": to_date}}


class AccountFilter(BaseFilter):

    name = 'account_name'
    value_type = str
    allow_multiple = False

    @classmethod
    def condition(cls, account_name):
        return {
            'account': {
                "$regex": '.*?{}.*?'.format(account_name),
                "$options": 'si'
            }
        }


class NameFilter(BaseFilter):

    name = 'name'
    value_type = str
    allow_multiple = False

    @classmethod
    def condition(cls, name):
        return {
            'name': {
                "$regex": '.*?{}.*?'.format(name),
                "$options": 'si'
            }
        }


class TagFilter(BaseFilter):

    name = 'tag'
    value_type = str
    allow_multiple = True

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

