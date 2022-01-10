from .models import Newsletter
from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    website = forms.URLField(max_length=80)


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email', )


class ContactForm(forms.Form):
    name = forms.CharField(max_length=20)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
