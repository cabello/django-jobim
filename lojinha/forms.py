from django import forms

from lojinha.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('read',)


class BidForm(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=5000)
    email = forms.EmailField(max_length=128)
