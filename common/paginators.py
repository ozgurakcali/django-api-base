from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class NormalizedLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom paginator, to return results in "body" key instead of "results" key
    """

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pagination', OrderedDict([
                ('count', self.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link())
            ])),
            ('body', data)
        ]))
