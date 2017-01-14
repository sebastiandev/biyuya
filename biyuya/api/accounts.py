from .base import BaseResource
from ..models.account import Account
from ..models.filters import NameFilter


class Accounts(BaseResource):

    model = Account
    filters = [NameFilter]

    def post(self):
        Account.add(Account(self.json_request))
        return {}, 201

    def delete(self, ids):
        Account.delete(*ids.split(','))
        return {}, 204
