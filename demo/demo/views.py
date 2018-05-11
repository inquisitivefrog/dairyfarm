from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.views import generic

from demo.forms import ContactForm

def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
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
               'Your website' + '',
               ['your_email@gmail.com'],
               headers = {'Reply=To': contact_email}
            )
            email.send()
            return redirect('contact')

    return render(request, 'demo/contact.html', {
        'form': form_class,
    })

def redirect(request):
    destination = '/summary/'
    return HttpResponseRedirect(destination)

class IndexView(generic.ListView):
    queryset = User.objects.all()
    template_name = 'demo/index.html'

