from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic

def redirect(request):
    destination = '/summary/'
    return redirect(destination)

class IndexView(generic.ListView):
    queryset = User.objects.all()
    template_name = 'demo/index.html'

