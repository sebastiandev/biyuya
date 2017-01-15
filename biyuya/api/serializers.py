from flask_restful import fields, marshal
from ..models.expense import Expense


class ModelSerializer(object):

    output = None
    input = None

    @classmethod
    def serialize(cls, data):
        return marshal(data, cls.output)


class PlainExpenseSerializer(ModelSerializer):

    output = {
        'date': fields.DateTime(dt_format='iso8601'),
        'amount': fields.Float(),
        'tags': fields.List(fields.String),
        'account': fields.String(),
        'note': fields.String()
    }


class MonthlyExpenseSerializer(ModelSerializer):

    months_serializer = {
        'month': fields.Integer(),
        'amount': fields.Integer()
    }

    output = {
        'date': fields.DateTime(dt_format='iso8601'),
        'amount': fields.Float(),
        'tags': fields.List(fields.String),
        'account': fields.String(),
        'note': fields.String(),
        'months': fields.List(fields.Nested(months_serializer)),
        'total_months': fields.Integer()
    }


class ExpenseSerializer(ModelSerializer):

    @classmethod
    def serialize(cls, data):
        res = []
        for d in data if type(data) is list else [data]:
            if d.type == Expense.type:
                serializer = PlainExpenseSerializer.output
            else:
                serializer = MonthlyExpenseSerializer.output

            res.append(marshal(d, serializer))

        return res


class AccountSerializer(ModelSerializer):

    output = {
        'name': fields.String(),
        'currency': fields.String(),
        'note': fields.String(),
    }


