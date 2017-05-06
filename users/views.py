from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from notes.models import Note


def index(request):
    return render(request, 'users/index.html', {})


class SignupView(generic.View):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            return render(
                request,
                self.template_name,
                {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            new_user = authenticate(username=username, password=password, )
            login(request, new_user)
            return HttpResponseRedirect(reverse('notes:index'))
        return render(request, self.template_name, {'form': form})


class ProfileView(generic.DetailView):
    model = User
    template_name = 'users/profile.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            notes = Note.objects.filter(author=request.user).order_by('-pub_date')
            return render(request, self.template_name, {'notes': notes})
        return HttpResponseRedirect(reverse('notes:index'))
