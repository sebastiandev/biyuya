import yaml
import logging
import json
import os
import flask_restful
from flask import Blueprint, jsonify, make_response
from pymongo import MongoClient
from biyuya import app


def load_conf(conf_def):
    return yaml.load(open(conf_def)) if type(conf_def) is str else conf_def


class Conf(dict):

    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError("%s doesn't have attribute '%s'" % (self.__class__.__name__, key))

    def __setattr__(self, name, val):
        self[name] = Conf(**val) if type(val) is dict else val


class ApiFactory(object):

    @staticmethod
    def _load_api_conf():
        db_conf = app.config['DATABASE']
        return Conf(**{
            'database': MongoClient(db_conf['uri'])[db_conf['name']]
        })

    @staticmethod
    def build():
        def load_resource_class(class_path):
            parts = class_path.split('.')
            module = ".".join(parts[:-1])
            m = __import__(module)

            for comp in parts[1:]:
                m = getattr(m, comp)

            return m

        endpoints = load_conf(app.config['ENDPOINTS'])

        api_blueprint = Blueprint('Api', __name__, url_prefix="/api")
        api_blueprint.conf = ApiFactory._load_api_conf()
        rest_api = RestApi(app=api_blueprint)

        for endpoint in endpoints:
            rest_api.add_resource(load_resource_class(endpoint['class']),
                                  *endpoint['urls'],
                                  endpoint=endpoint['name'],
                                  resource_class_kwargs=api_blueprint.conf)

        return api_blueprint


class ApiException(Exception):

    GET = 'get'
    POST = 'post'
    PATCH = 'patch'
    DELETE = 'delete'

    @property
    def data(self):
        return {
            'status': self.status,
            'detail': self.detail,
            'title': self.title,
            'meta': self.meta if hasattr(self, 'meta') else {}
        }


class RestApi(flask_restful.Api):

    MEDIA_TYPE = 'application/json'
    DEFAULT_HEADER = {'Content-Type': MEDIA_TYPE}

    def __init__(self, app, prefix='', mediatype=MEDIA_TYPE, errors=None, decorators=None):
        super(RestApi, self).__init__(app=app,
                                      prefix=prefix,
                                      default_mediatype=mediatype,
                                      decorators=decorators,
                                      errors=errors)

        @app.route('/')
        def main():
            return jsonify({
                'name': 'biyuya-api',
                'version': '0.0.1',
            })

    def handle_error(self, e):
        if isinstance(e, ApiException):
            error_response = self.output_json(e.data, e.status)
            error_response = '{}' if e.status == 200 else error_response

        else:
            error_response = super(RestApi, self).handle_error(e)

        return error_response
