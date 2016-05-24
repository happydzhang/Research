# Brian Mann
# 5/24/2016

import cherrypy
import webbrowser, urllib2, time, datetime, json, requests

class OptionsController:
        def OPTIONS(self, *args, **kwargs):
                return ""

def CORS():
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
        cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

def start_service():
        dispatcher = cherrypy.dispatch.RoutesDispatcher()
	optionsController = OptionsController()

	conf = {
                'global': {
                        'server.socket_host': '0.0.0.0'
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
