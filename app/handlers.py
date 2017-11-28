import webapp2
import logging

import config

__all__ = [
    'WWWizeHandler',
]


BAD_GATEWAY_RESPONSE = """
<!doctype html><html><body><h1>Bad Gateway</h1></body></html>
""".strip()

BAD_REQUEST_RESPONSE = """
<!doctype html><html><body><h1>Bad Response</h1></body></html>
""".strip()


class WWWizeHandler(webapp2.RequestHandler):
    def handle_request(self):
        domain = self.request.host

        if domain.startswith('www.'):
            logging.error(
                "Failed to wwwize: request already has 'www.' prefix "
                "(domain: %s)",
                domain
            )

            self.response.set_status(403)
            self.response.write(BAD_REQUEST_RESPONSE)

            return

        if not is_valid_domain(domain):
            self.response.set_status(502)
            self.response.write(BAD_GATEWAY_RESPONSE)

            return

        redirect_url = get_redirect_url(self.request)

        self.redirect(redirect_url, code=307)

    get = handle_request
    put = handle_request
    post = handle_request
    head = handle_request
    delete = handle_request
    options = handle_request
    patch = handle_request
    connect = handle_request


def is_valid_domain(domain):
    if not config.DOMAINS:
        return True

    return domain in config.DOMAINS


def get_redirect_url(request):
    scheme = 'https' if config.FORCE_HTTPS else request.scheme

    return '{}://{}{}'.format(
        scheme,
        'www.' + request.host,
        request.path_qs
    )
