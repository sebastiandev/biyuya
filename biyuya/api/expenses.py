from .base import BaseResource
from ..models.expense import Expense, MonthlyExpense, ExpenseFactory
from ..models.filters import TagFilter, AccountFilter, DateFilter, DateRangeFilter
from .serializers import ExpenseSerializer


class Expenses(BaseResource):

    model = Expense
    serializer = ExpenseSerializer
    filters = [TagFilter, AccountFilter, DateFilter, DateRangeFilter]

    def get_all(self):
        """ Override to include monthly expenses as well"""
        return list(Expense.all()) + list(MonthlyExpense.all())

    def post(self):
        Expense.add(ExpenseFactory.build(self.json_request))
        return {}, 201

    def delete(self, ids):
        Expense.delete(*ids.split(','))
        return {}, 204
