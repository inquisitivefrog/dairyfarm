from django.contrib.auth.models import User
from django.views import generic

class IndexView(generic.ListView):
    queryset = User.objects.all()
    template_name = 'demo/index.html'

