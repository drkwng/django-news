from django.shortcuts import render
from userena.views import signin, signup
from django.http import HttpResponse

from .models import Author


def author_profile_detail(request,  **kwargs):
    user = Author.objects.get(user__username=kwargs.get('username'))
    context = {'user': user}
    print(locals())
    return render(request, 'authors/base-author.html', context)


def custom_signin(request, *args, **kwargs):
    if request.POST:
        return signin(request, *args, **kwargs)
    else:
        return HttpResponse(status=404)


def custom_signup(request, *args, **kwargs):
    if request.POST:
        return signup(request, *args, **kwargs)
    else:
        return HttpResponse(status=404)
