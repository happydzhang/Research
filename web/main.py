# Brian Mann
# 5/24/2016

import cherrypy
from data import DataController

class OptionsController:
        def OPTIONS(self, *args, **kwargs):
                return ""

def CORS():
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
        cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

def start_service():
        dispatcher = cherrypy.dispatch.RoutesDispatcher()
	dataController = DataController()
	optionsController = OptionsController()

	dispatcher.connect('data_post', '/data/', controller=dataController, action = 'POST', conditions=dict(method=['POST']))

	dispatcher.connect('data_option', '/data/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))

	conf = {
                'global': {
                        'server.socket_host': '0.0.0.0',
			'server.socket_port': 8008
                },
                '/': {
                        'request.dispatch': dispatcher,
                        'tools.CORS.on': True,
                }
        }

        cherrypy.config.update(conf)
        app = cherrypy.tree.mount(None, config=conf)
        cherrypy.quickstart(app)

if __name__ == '__main__':
        cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
        start_service()
