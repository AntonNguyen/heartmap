from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import models
base = ''

def index(request):
	t = loader.get_template('dating/index.html')
	c = Context({
		"base" : base
	})
	return HttpResponse(t.render(c))

def signup(request):

	if request.POST:
		username = request.POST.get("username")
		password = request.POST.get("password")
		email = request.POST.get("email")
		user = User.objects.create_user(username, email, password)
		user.save()

		birthday = request.POST.get("birthday")
		gender = request.POST.get("sex")
		seeking = request.POST.get("seeking")
		phone = request.POST.get("phone")

		profile = user.get_profile()
		profile.gender = gender
		profile.seeking = seeking
		profile.birthday = birthday
		profile.phone = phone
		profile.save()

		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)
		return HttpResponseRedirect(base + "/matches/")
	else:
		return HttpResponseRedirect(base + "/")

def do_login(request):
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(base + "/matches/")

	return HttpResponseRedirect(base + "/")

@login_required
def do_logout(request):
	logout(request)
	return HttpResponseRedirect(base + "/")

@login_required
def matches(request):
	t = loader.get_template('dating/matches.html')
	c = Context({
		"base" : base,
		"person" : request.user,
		"users" : User.objects.all().exclude(id=request.user.id)
	})
	return HttpResponse(t.render(c))


@login_required
def match(request, match_id):
	from django.utils import simplejson
	import urllib2

	# Get User
	user = User.objects.get(id=match_id)

	# Get Flowers
	url = "http://api.sandbox.yellowapi.com/FindBusiness/?what=florists&where=Toronto&UID=127.0.0.1&apikey=djesz8tau27gh528rr7p34fn&fmt=json"

	json = urllib2.urlopen(url).read()
	json = simplejson.loads(json)
	florist = json['listings'][0]

	# Build Template
	t = loader.get_template('dating/profile.html')
	c = Context({
		"base" : base,
		"user" : user,
		"florist" : florist
	})

	return HttpResponse(t.render(c))

@login_required
def me(request):
	return HttpResponse("me")

@login_required
def outgoing(request):
	from twilio.rest import TwilioRestClient

	caller_id = "+16479311254"

	first_number = "+1" + request.GET.get("first_caller")
	second_number = "+1" + request.GET.get("second_caller")

	account_sid = "AC8ff5d5559906452dac072725264d5863"
	auth_token = "edd564df902310a3354ec1e77605fadd"

	client = TwilioRestClient(account_sid, auth_token)
	first_call = client.calls.create(to=first_number,
							   from_=caller_id,
							   method="GET",
							   url="http://afn85.webfactional.com/hackto/connect/?room=FreshBooks_" + str(first_number) + str(second_number))

	second_call = client.calls.create(to=second_number,
							   from_=caller_id,
							   method="GET",
							   url="http://afn85.webfactional.com/hackto/connect/?room=FreshBooks_" + str(first_number) + str(second_number))

	return HttpResponseRedirect(base + "/matches/")

def connect(request):
	import twilio.twiml

	room = request.GET.get("room")

	resp = twilio.twiml.Response()
	resp.say("You are now entering the conference line.")
	with resp.dial() as g:
		g.conference(room)
	return HttpResponse(str(resp), mimetype="application/xml")