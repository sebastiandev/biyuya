from .base import BaseResource
from ..models.expense import Expense, MonthlyExpense, ExpenseFactory
from ..models.filters import TagFilter, AccountFilter, DateFilter, DateRangeFilter
import arrow


class Expenses(BaseResource):

    model = Expense
    filters = [TagFilter, AccountFilter, DateFilter, DateRangeFilter]

    def get_all(self):
        """ Override to include monthly expenses as well"""
        return list(Expense.all()) + list(MonthlyExpense.all())

    def _filter_by_date_range(self):
        dates = self.requested_filters.date_range_filter.split(',')
        date_from_filter = arrow.get(dates[0], 'YYYYMMDD').to('utc')
        date_to_filter = arrow.get(dates[1], 'YYYYMMDD').to('utc')
        print("Filtering expenses by date range..")
        return list(Expense.by_date_range(date_from_filter.format('YYYY-MM-DD'),
                                          date_to_filter.format('YYYY-MM-DD')))

    def post(self):
        Expense.add(ExpenseFactory.build(self.json_request))
        return {}, 201

    def delete(self, ids):
        Expense.delete(*ids.split(','))
        return {}, 204
