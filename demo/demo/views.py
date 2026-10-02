from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views import generic
from django.views.decorators.http import require_POST

from demo.forms import ContactForm

def contact(request):
    form_class = ContactForm
    form = form_class(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            form_content = form.cleaned_data['content']
            template = get_template('demo/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
               'new contact form submission',
               content,
               settings.DEFAULT_FROM_EMAIL,
               [settings.CONTACT_EMAIL],
               reply_to=[contact_email]
            )
            email.send()
            return HttpResponseRedirect('/contact/')

    return render(request, 'demo/contact.html', {'form': form})

def redirect(request):
    destination = '/summary/'
    return HttpResponseRedirect(destination)

def ui_login(request):
    return render(request, 'registration/ui_login.html', {})

@login_required
def ui_logged_in(request):
    clients = [
        {'id': client.id, 'name': client.name}
        for client in request.user.client_set.all()
    ]
    data = {"user": {"id": request.user.id,
                     "username": request.user.username,
                     "first_name": request.user.first_name,
                     "last_name": request.user.last_name,
                     "email": request.user.email,
                     "client": clients[0] if clients else None,
                     "clients": clients},
            "auth": None}
    return JsonResponse(data)

@login_required
@require_POST
def ui_logout(request):
    logout(request)
    return JsonResponse({'detail': 'Logged out.'})

class IndexView(generic.ListView):
    queryset = User.objects.all()
    template_name = 'demo/index.html'
