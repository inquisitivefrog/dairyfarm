from django.forms import CharField, EmailField, Form, Textarea

class ContactForm(Form):
    contact_name = CharField(required=True)
    contact_email = EmailField(required=True)
    content = CharField(required=True,
                        widget=Textarea)
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = 'Your name:'
        self.fields['contact_email'].label = 'Your email:'
        self.fields['content'].label = 'What do you want to say?'
