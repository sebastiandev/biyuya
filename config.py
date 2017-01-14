# API CONF
ENDPOINTS = [{
    'name': 'expenses',
    'class': 'biyuya.api.expenses.Expenses',
    'urls': [
        '/expenses',
        '/expenses/<string:ids>'
    ]}, {
    'name': 'accounts',
    'class': 'biyuya.api.accounts.Accounts',
    'urls': [
        '/accounts',
        '/accounts/<string:ids>'
    ]}
]

# DATABASE
DATABASE = {
    'uri': 'mongodb://localhost:27017/',
    'name': 'biyuya'
}

