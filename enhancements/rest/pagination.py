from rest_framework.pagination import CursorPagination, _positive_int


class EnhancedCursorPagination(CursorPagination):

    limit_query_param = 'limit'
    max_limit = None

    def get_page_size(self, request):
        if self.limit_query_param:
            try:
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        return self.page_size