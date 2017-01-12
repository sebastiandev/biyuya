from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


@app.route("/")
def main():
    return "biyuya-server"


from .api import ApiFactory

app.register_blueprint(ApiFactory().build())
