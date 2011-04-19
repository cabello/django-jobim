from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template

from lojinha.models import Bid, Contact


class ContactForm(forms.ModelForm):
    def save(self, commit=True):
        super(ContactForm, self).save(commit)
        mail_context = Context(self.cleaned_data)
        send_mail(
            get_template('contact_subject.txt').render(mail_context),
            get_template('contact_message.txt').render(mail_context),
            self.cleaned_data['email'],
            [settings.CONTACT_EMAIL]
        )

    class Meta:
        model = Contact
        exclude = ('read',)


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ('product', 'accepted')
