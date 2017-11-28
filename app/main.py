import webapp2

import config

__all__ = [
    'app',
]

routes = [
    (r'/.*', 'handlers.WWWizeHandler'),
]


app = webapp2.WSGIApplication(
    routes=routes,
    debug=False,
    config=config.__dict__,
)
