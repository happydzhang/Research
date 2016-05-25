# Brian Mann
# data.py
# 5/25/2016

import cherrypy, requests
import re, json
import webbrowser, urllib2, time, datetime

class DataController(object):
	def __init__(self):
		pass

	def GET(self):
		output = {'result':'success'}
		return json.dumps(output, encoding='latin-1')

	def POST(self):
		output = {'result':'success'}
		try:
			params = cherrypy.request.body.read()
			data = json.loads(params)
			location = data['location']
			srange = data['range']
			section = data['section']
			query = data['query']
			limit = data['limit']
			print data
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')
