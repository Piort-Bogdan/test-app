from drf_spectacular_jsonapi.schemas.pagination import JsonApiPageNumberPagination


class CustomJsonApiPageNumberPagination(JsonApiPageNumberPagination):
    page_query_param = 'page_number'
    page_size_query_param = None
    max_page_size = None
