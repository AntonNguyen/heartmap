from django.http import HttpResponse
from django.template import Context, loader

def index(request):
	t = loader.get_template('dating/index.html')
	c = Context({
		'name' : 'Anton'
	})
	return HttpResponse("hello")

def incoming(request):
	import twilio.twiml
	import string

	callers = {
		"+16476698275" : "Anton Nguyen",
		"+16473099891" : "Rae Chao Jin Qu"
	}

	queries = dict(zip(map(string.lower, request.GET.keys()), request.GET.values()))

	response = "Hello Monkey!"
	resp = twilio.twiml.Response()

	from_number = queries.get('from', '')
	if from_number != '':
		for number in callers:
			print number.find(str(from_number))
			if number.find(from_number) > -1:
				response = "Hello " + callers[number]
				break

	resp.say(response)

	return HttpResponse(str(resp), mimetype="application/xml")

def outgoing(request):
	from twilio.rest import TwilioRestClient

	caller_id = "+16479311254"

	account_sid = "AC8ff5d5559906452dac072725264d5863"
	auth_token = "edd564df902310a3354ec1e77605fadd"

	client = TwilioRestClient(account_sid, auth_token)
	first_call = client.calls.create(to="+16473099891",
							   from_=caller_id,
							   url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient",
							   status_callback="http://afn85.webfactional.com/hackto/connect/")

	second_call = client.calls.create(to="+6476698275",
							   from_=caller_id,
							   url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient",
							   status_callback="http://afn85.webfactional.com/hackto/connect/")

	return HttpResponse("Ok!")

def connect(request):
	import twilio.twiml

	resp = twilio.twiml.Response()
	resp.say("You are now entering the conference line.")
	with resp.dial() as g:
		g.conference("hello")
	return HttpResponse(str(resp), mimetype="application/xml")