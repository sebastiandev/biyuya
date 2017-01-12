

class JSONSerializer(object):

    attrs = {}

    def serialize(self, model):
        data = {}
        for attr, attr_type in self.attrs.items():
            if attr_type == list:
                data[attr] = [str(e) for e in model.get(attr)]

            elif type(attr_type) is list:
                element_list = model.get(attr)
                list_data = []

                for e_name, e_type in attr_type.items():
                    for e in element_list:
                        list_data.append({e.get(e_name): e_type(e)})

                data[attr] = list_data

            else:
                data[attr] = attr_type(model.get(attr))

        return data


class ExpenseSerializer(JSONSerializer):

    attrs = {
        'date': str,
        'amount': int,
        'tags': list,
        'account': str,
        'note': str
    }


class MonthlyExpenseSerializer(JSONSerializer):

    attrs = {
        'date': str,
        'amount': int,
        'tags': list,
        'account': str,
        'note': str,
        'months': [{
            'month': int,
            'amount': int
        }],
        'total_months': int
    }


class AccountSerializer(JSONSerializer):

    attr = {
        'name': str,
        'currency': str,
        'note': str
    }
