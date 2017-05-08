from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from notes.forms import NoteForm, LabelForm
from notes.models import Note, Label


class IndexView(generic.ListView):
    template_name = 'notes/index.html'
    context_object_name = 'latest_notes_list'

    def get_queryset(self):
        queryset = Note.objects.all()

        label_param = self.request.GET.get('label')
        user_param = self.request.GET.get('user')
        queryset = queryset.filter(public=True)
        if label_param is not None:
            queryset = queryset.filter(labels__text=label_param)
        if user_param is not None:
            queryset = queryset.filter(author__username=user_param)
        return queryset.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Note
    template_name = 'notes/detail.html'

    def get_queryset(self):
        """ Exclude notes that haven't been published yet """
        user_param = self.request.user
        queryset = Note.objects.filter(author__username=user_param)
        return queryset.filter(pub_date__lte=timezone.now())


class ComposeLabelView(generic.CreateView):
    model = Label
    form_class = LabelForm
    template_name_suffix = '_new_form'
    success_url = '/users/profile'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            if Label.objects.filter(text=form.cleaned_data['text']).exists():
                messages.warning(request, "Label already exists")
                # raise ValidationError("This label already exists")
            else:
                label.save()
                messages.success(request, "Label successfully saved")

        else:
            messages.error(request, "Invalid Form")
            # raise ValidationError("Invalid Form")
        return HttpResponseRedirect(reverse('users:profile'))


class ComposeView(generic.CreateView):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_compose_form'

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.object.id})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.pub_date = timezone.now()
            note.author = request.user
            note.save()
            form.save_m2m()
            return HttpResponseRedirect(
                reverse('notes:detail', kwargs={'pk': note.id}))


class EditView(generic.UpdateView):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.object.id})


class DeleteView(generic.DeleteView):
    model = Note
    success_url = '/users/profile'
