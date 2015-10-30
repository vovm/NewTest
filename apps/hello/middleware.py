from .models import AllRequest


class RequestMiddleware(object):
    def process_request(self, request):
        req2 = AllRequest()
        req2.method = request.method
        req2.path = request.path
        if req2.path != '/request/ajax_request_list':
            req2.save()
