from rest_framework import pagination
from rest_framework.response import Response

class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(data=data, headers={'Total-Pages': self.page.paginator.num_pages})
