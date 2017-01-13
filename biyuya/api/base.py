from flask_restful import Resource, reqparse, request
import urllib
from .response import ResponseFactory


class BaseResource(Resource):

    INCLUDE_ARG = 'include'
    PAGE_NUMBER_ARG = 'page[number]'
    PAGE_SIZE_ARG = 'page[size]'
    SORT_ARG = 'sort'

    FILTERS = []

    def __init__(self, *args, **kwargs):
        super(BaseResource).__init__()
        self._base_url = request.base_url
        self._api_url = request.url_root + 'api'
        self._db = kwargs.get('database')

        self._parser = reqparse.RequestParser()
        self._parser.add_argument(self.INCLUDE_ARG, type=str)
        self._parser.add_argument(self.PAGE_NUMBER_ARG, type=int, dest='page_number')
        self._parser.add_argument(self.PAGE_SIZE_ARG, type=int, dest='page_size')
        self._parser.add_argument(self.SORT_ARG, type=str)

        for filter_def in self.FILTERS:
            self._parser.add_argument('filter[{}]'.format(filter_def['name']),
                                      type=filter_def['type'],
                                      dest=filter_def['alias'])

        self._args = self._parser.parse_args()

    @property
    def requested_filters(self):
        args = dict(self._args)
        args.pop('include')
        args.pop('page_number')
        args.pop('page_size')
        args.pop('sort')
        return reqparse.Namespace(**args)

    def base_url_without_params(self, params):
        return self._base_url.replace('/' + params, '')

    @property
    def json_request(self):
        return request.json

    @property
    def api_endpoint(self):
        return self._base_url.replace(self._api_url, '')

    @property
    def url_query_string(self):
        return urllib.parse.unquote_plus(request.query_string)

    @property
    def include_param(self):
        return self._args.include.split(',') if self._args.include else []

    @property
    def page_number_param(self):
        return self._args.page_number

    @property
    def page_size_param(self):
        return self._args.page_size

    def build_response(self, data, included, meta={}, pagination=None):
        if pagination:
            meta.update(self.build_pagination_info(pagination))

        response = ResponseFactory.data_response(data=data, meta=meta, included=included)
        # response.links = LinkItem(base_url=self._api_url,
        #                           resource=self.endpoint,
        #                           pagination=pagination).serialize()

        return response
