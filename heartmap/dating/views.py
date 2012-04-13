from django.http import HttpResponse
from django.template import Context, loader

def index(request):
	t = loader.get_template('dating/index.html')
	c = Context({
		'name' : 'Anton'
	})
	return HttpResponse("hello")

def twilio(request):
	import twilio.twiml

	resp = twilio.twiml.Response()
	resp.say("Hello Rae!")
	return HttpResponse(str(resp), mimetype="application/xml")