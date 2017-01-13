

class JSONSerializer(object):

    fields = {}

    def serialize(self, model):
        data = {}
        for name, field_type in self.fields.items():
            if field_type == list:
                data[name] = [str(e) for e in model.get(name)]

            # No support for embedded collection of collection. Only one level
            elif type(field_type) is list:
                element_list = model.get(name)
                list_data = []

                for e_name, e_type in field_type.items():
                    for e in element_list:
                        list_data.append({e.get(e_name): e_type(e)})

                data[name] = list_data

            else:
                data[name] = field_type(model.get(name))

        return data


class ExpenseSerializer(JSONSerializer):

    fields = {
        'date': str,
        'amount': int,
        'tags': list,
        'account': str,
        'note': str
    }


class MonthlyExpenseSerializer(JSONSerializer):

    fields = {
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

    fields = {
        'name': str,
        'currency': str,
        'note': str
    }
