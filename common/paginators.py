from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class HeaderLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom paginator, to return pagination data in response headers
    """

    def get_paginated_response(self, data):
        headers = {
            'Pagination-Count': self.count
        }

        # Build page headers for pagination
        if self.get_next_link():
            headers['Pagination-Next'] = self.get_next_link()
        if self.get_previous_link():
            headers['Pagination-Previous'] = self.get_previous_link()

        return Response(data, headers=headers)
