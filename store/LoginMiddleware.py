class LoginMiddleware(object):
    @staticmethod
    def process_request(request):
        pass_urls = ['', 'store/login', 'back', 'back/login', 'back/error']
        if pass_urls.__contains__(request.path) or request.session.get("staff_id", default=None) is not None:
            pass
