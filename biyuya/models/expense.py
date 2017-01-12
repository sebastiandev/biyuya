from . import BaseModel, ObjectDict


class ExpenseFactory(object):

    @staticmethod
    def build(data):
        if data.get('type') == Expense.type:
            return Expense(**data)

        elif data.get('type') == MonthlyExpense.type:
            return MonthlyExpense(**data)

        elif int(data.get('total_months', 0)) > 0 and int(data.get('partial_amount', 0)) > 0:
            return MonthlyExpense(**data)

        else:
            if 'month' in data:
                data.pop('month')

            if 'total_months' in data:
                data.pop('total_months')

            if 'partial_amount' in data:
                data.pop('partial_amount')

            return Expense(**data)


class Expense(BaseModel):

    type = 'plain_expense'
    collection_name = 'expenses'

    def __init__(self, date=None, amount=0, tags=None, account=None, notes=None, **kwargs):
        if 'type' in kwargs:
            kwargs.pop('type')

        super().__init__(**{
            'type': Expense.type,
            'date': date,
            'amount': int(amount),
            'tags': tags or [],
            'account': account,
            'notes': notes
        }, **kwargs)

    @classmethod
    def _build_entity(cls, doc):
        return ExpenseFactory.build(doc)

    @classmethod
    def by_account(cls, account_name):
        for d in cls._collection().find({
            'account': {
                "$regex": '/.*?{}.*?/i'.format(account_name),
                "$options": 's'
            }
        }):
            yield cls._build_entity(d)

    @classmethod
    def by_date(cls, date):
        for d in cls._collection().find({'date': date}):
            yield cls._build_entity(d)

    @classmethod
    def by_date_range(cls, from_date, to_date):
        for d in cls._collection().find({'date': {"$gte": from_date, "$lte": to_date}}):
            yield cls._build_entity(d)

    @classmethod
    def by_tag(cls, *tags):
        for d in cls._collection().find({
            'tags': {
                "$elemMatch": {
                    "$regex": '/.*?{}.*?/i'.format('|'.join(tags)),
                    "$options": 's'
                }
            }
        }):
            yield cls._build_entity(d)


class InvalidMonthlyExpense(Exception):
    pass


class MonthlyExpense(Expense):

    type = 'monthly_expense'

    def __init__(self, date=None, amount=0, total_months=0, partial_amount=0, tags=None, account=None, notes=None, **kwargs):
        super().__init__(**{
            'type': MonthlyExpense.type,
            'date': date,
            'amount': int(amount),
            'tags': tags or [],
            'account': account,
            'notes': notes,
            'months': [ObjectDict(**{
               'month': 1,
               'date': date,
               'amount': int(partial_amount)
            })],
            'total_months': int(total_months),
        }, **kwargs)

    def add_expense(self, date, amount):
        month_number = len([1 for _ in self.months])
        if month_number > self.total_months:
            raise InvalidMonthlyExpense("Can't add more expenses than the main expense total months")

        self.months.append({
            'month': int(month_number),
            'date': date,
            'amount': int(amount)
        })

    @classmethod
    def pending_expenses(cls):
        res = cls._collection().aggregate([{
            "$match": {
                'total_months': {"$gte": 1}
            }
        }, {
            "$project": {
                'month': '$months.month',
                'total_months': 1}
        }, {
            "$project": {
                'last_pay': {"$max": '$month'},
                'total_months': 1
            }
        }, {
            "$project": {
                'pending': {"$gt": ["$total_months", "$last_pay"]}
            }
           }, {
            "$match": {
                'pending': True
            }
        }])

        for r in res:
            yield cls._build_entity(cls._collection().find_one({'_id': r['_id']}))
