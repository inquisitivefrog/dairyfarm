from django.views import generic

from assets.models import Cow

class IndexView(generic.ListView):
    queryset = Cow.objects.all()
    template_name = 'assets/index.html'
