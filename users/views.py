# import requests


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from notes.models import Note, Label
from notes.views import search
from util import isNotBlank


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
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # recaptcha_response = request.POST.get('g-recaptcha-response')
            # data = {
            #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            #     'response': recaptcha_response
            # }
            # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            # result = r.json()
            # print(result)
            # ''' End reCAPTCHA validation '''

            # if result['success']:
            new_user = authenticate(username=username, password=password, )
            user.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse('users:profile'))
        return render(request, self.template_name, {'form': form})


class ProfileView(generic.DetailView):
    model = User
    template_name = 'users/profile.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            search_param = self.request.GET.get('q')
            notes_non_archived = Note.objects.filter(author=request.user).filter(archived=False).order_by('-updated')
            notes_archived = Note.objects.filter(author=request.user).filter(archived=True).order_by('-updated')
            if isNotBlank(search_param):
                MODEL_MAP = {Note: ["note_title", "note_text", "labels__text"], }
                notes_non_archived = search(search_param, notes_non_archived, MODEL_MAP)
            labels = Label.objects.filter(author__username=request.user)
            return render(request, self.template_name,
                          {'notes': notes_non_archived, 'labels': labels, 'notes_archived': notes_archived})
        return HttpResponseRedirect(reverse('notes:index'))
