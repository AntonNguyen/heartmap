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

	callers = {
		"+16476698275" : "Anton Nguyen",
		"+16473099891" : "Rae Chao Jin Qu"
	}

	response = "Hello Monkey!"
	resp = twilio.twiml.Response()

	if 'from' in request.GET:
		from_number = request.GET['from']
		if from_number in callers:
			response = "Hello " + callers[from_number]

	resp.say(response)

	return HttpResponse(str(resp), mimetype="application/xml")