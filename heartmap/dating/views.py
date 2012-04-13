from django.http import HttpResponse
from django.template import Context, loader

def index(request):
	t = loader.get_template('dating/index.html')
	c = Context({
		'name' : 'Anton'
	})
	return HttpResponse(t.render(c))
