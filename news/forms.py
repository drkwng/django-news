from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    website = forms.URLField(max_length=80)


class SubscriptionForm(forms.Form):
    email = forms.EmailField()