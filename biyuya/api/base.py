from flask_restful import Resource, reqparse, request
import urllib
from .response import ResponseFactory


class BaseResource(Resource):

    model = None
    filters = []

    INCLUDE_ARG = 'include'
    PAGE_NUMBER_ARG = 'page[number]'
    PAGE_SIZE_ARG = 'page[size]'
    SORT_ARG = 'sort'

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

        for filter_cls in self.filters:
            self._parser.add_argument('filter[{}]'.format(filter_cls.name.replace('_', '-')),
                                      dest=filter_cls.name,
                                      type=filter_cls.value_type)

        self._args = self._parser.parse_args()

    @property
    def requested_filters(self):
        filters_by_name = {f.name: f for f in self.filters}

        return reqparse.Namespace(**{
            k: reqparse.Namespace(**{
                'filter_cls': filters_by_name[k],
                'value': v
            }) for k, v in self._args.items() if k in filters_by_name and v})

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

    def get(self, ids=None):
        included = []
        meta = {}
        filters = self.requested_filters

        if ids:
            data = self.get_by_ids(ids)

        elif filters:
            data = self.get_by_filters(filters)

        else:
            data = self.get_all()

        return self.build_response(data=data, included=included, meta=meta).data()

    def get_by_ids(self, ids):
        return self.model.by_id(ids[0])

    def get_by_filters(self, filters):
        # TODO: move filter parsing and loading to a separate module, maybe FiltrableResource
        if len(filters) > 1:
            condition = {}
            for filter_def in filters.values():
                filter_class = filter_def.filter_cls

                if filter_class.allow_multiple:
                    condition.update(filter_class.condition(*filter_def.value.split(',')))

                else:
                    condition.update(filter_class.condition(filter_def.value))

            data = list(self.model.find(condition))

        else:
            filter_def = list(filters.values())[0]
            filter_class = filter_def.filter_cls

            if filter_class.allow_multiple:
                data = list(filter_class.apply(self.model, *filter_def.value.split(',')))

            else:
                data = list(filter_class.apply(self.model, filter_def.value))

        return data

    def get_all(self):
        return list(self.model.all())
