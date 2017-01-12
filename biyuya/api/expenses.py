from .base import BaseResource
from ..models.expense import Expense, MonthlyExpense, ExpenseFactory


class Expenses(BaseResource):

    def get(self, ids=None):
        included = []
        meta = {}

        if ids:
            data = Expense.by_id(ids[0])

        else:
            data = list(Expense.all()) + list(MonthlyExpense.all())

        return self.build_response(data=data, included=included, meta=meta).data()

    def post(self):
        e = ExpenseFactory.build(self.json_request)
        print(e)

    def delete(self, ids=None):
        pass
