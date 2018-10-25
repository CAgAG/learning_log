from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def logout_view(requst):
    """注销用户"""
    logout(requst)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(requst):
    if requst.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=requst.POST)

        if form.is_valid():
            new_user = form.save()

            authenticated_user = authenticate(username=new_user.username, password=requst.POST['password1'])
            login(requst, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(requst, 'users/register.html', context)