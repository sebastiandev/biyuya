from .base import BaseResource
from ..models.expense import Expense, MonthlyExpense, ExpenseFactory
from ..models.filters import TagFilter, AccountFilter, DateRangeFilter
import arrow


class Expenses(BaseResource):

    FILTERS = [{
        'name': 'by-date',
        'alias': 'date_filter',
        'type': str
    }, {
        'name': 'by-date-range',
        'alias': 'date_range_filter',
        'type': str
    }, {
        'name': 'by-tag',
        'alias': 'tag_filter',
        'type': str
    }]

    def get(self, ids=None):
        data = []
        included = []
        meta = {}

        if ids:
            data = Expense.by_id(ids[0])

        elif self.requested_filters:

            # If more than one filter specified, we have to combine them
            # use AttributFilters to combine conditions on a single find()
            
            if self.requested_filters.date_filter:
                data = self._filter_by_date()

            elif self.requested_filters.date_range_filter:
                data = self._filter_by_date_range()

            elif self.requested_filters.tag_filter:
                data = self._filter_by_tag()

        else:
            data = list(Expense.all()) + list(MonthlyExpense.all())

        return self.build_response(data=data, included=included, meta=meta).data()

    def _filter_by_tag(self):
        print("Filtering expenses by tag..")
        return list(Expense.by_tag(*self.requested_filters.tag_filter.split(',')))

    def _filter_by_date(self):
        date_to_filter = arrow.get(self.requested_filters.date_filter, 'YYYYMMDD').to('utc')
        print("Filtering expenses by date..")
        return list(Expense.by_date(date_to_filter.format('YYYY-MM-DD')))

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
