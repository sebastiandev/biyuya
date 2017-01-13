# API CONF
ENDPOINTS = [{
    'name': 'cis',
    'class': 'biyuya.api.expenses.Expenses',
    'urls': [
        '/expenses',
        '/expenses/<string:ids>'
    ]}
]

# DATABASE
DATABASE = {
    'uri': 'mongodb://localhost:27017/',
    'name': 'biyuya'
}

