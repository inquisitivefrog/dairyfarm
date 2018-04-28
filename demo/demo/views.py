from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views import generic

def redirect(request):
    return HttpResponseRedirect('/summary/')

class IndexView(generic.ListView):
    queryset = User.objects.all()
    template_name = 'demo/index.html'

