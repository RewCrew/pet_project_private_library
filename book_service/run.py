from wsgiref import simple_server
from composites.app_api import app

httpd = simple_server.make_server('0.0.0.0', 1235, app=app)
httpd.serve_forever()
