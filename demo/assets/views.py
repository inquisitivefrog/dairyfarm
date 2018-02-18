from django.views import generic

from assets.models import Cow

class IndexView(generic.ListView):
    context_object_name = 'herd'
    queryset = Cow.objects.all()
    template_name = 'assets/index.html'

class CowListView(generic.ListView, generic.CreateView):
    context_object_name = 'herd'
    queryset = Cow.objects.all()
    template_name = 'assets/cow_list.html'
