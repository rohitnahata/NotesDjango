from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from notes.forms import NoteForm, LabelForm, NoteArchiveForm
from notes.models import Note, Label


class IndexView(generic.ListView):
    template_name = 'notes/index.html'
    context_object_name = 'latest_notes_list'

    def get_queryset(self):
        queryset = Note.objects.all()
        user = self.request.user
        label_param = self.request.GET.get('label')
        user_param = self.request.GET.get('user')
        queryset = queryset.filter(Q(public=True) | Q(author__username=user)).filter(archived=False)
        if label_param is not None:
            queryset = queryset.filter(labels__text=label_param)
        if user_param is not None:
            queryset = queryset.filter(author__username=user_param)
        return queryset.filter(
            updated__lte=timezone.now(),
        ).order_by('-updated')


class DetailView(generic.DetailView):
    model = Note
    template_name = 'notes/detail.html'

    def get_queryset(self):
        return Note.objects.filter(updated__lte=timezone.now())

    def get_object(self, queryset=None):
        object = super(DetailView, self).get_object()
        queryset = Note.objects.filter(author__username=self.request.user)
        if queryset.count() > 0:
            return object
        queryset = Note.objects.filter(note_title__exact=object).filter(public=True).filter(archived=False)
        if queryset.count() > 0:
            return object
        else:
            return None


class ComposeLabelView(generic.CreateView):
    model = Label
    form_class = LabelForm
    template_name_suffix = '_new_form'
    success_url = '/users/profile'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            queryset = Label.objects.filter(user__username=request.user)
            if queryset.filter(text=form.cleaned_data['text']).exists():
                messages.warning(request, "Label already exists")
                # raise ValidationError("This label already exists")
            else:
                label.user = request.user
                label.save()
                messages.success(request, "Label successfully saved")
            return HttpResponseRedirect(reverse('users:profile'))


class ComposeView(generic.CreateView):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_compose_form'

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ComposeView, self).get_context_data(**kwargs)
        context['form'].fields['labels'].queryset = Label.objects.filter(user=self.request.user)
        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.archived = False
            note.save()
            form.save_m2m()
            return HttpResponseRedirect(
                reverse('notes:detail', kwargs={'pk': note.id}))


class EditView(generic.UpdateView):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['form'].fields['labels'].queryset = Label.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.object.id})


class EditLabelView(generic.UpdateView):
    model = Label
    form_class = LabelForm
    template_name_suffix = '_update_form'
    success_url = '/users/profile'


class DeleteView(generic.DeleteView):
    model = Note
    success_url = '/users/profile'


class DeleteLabelView(generic.DeleteView):
    model = Label
    success_url = '/users/profile'


class UnarchiveView(generic.UpdateView):
    model = Note
    form_class = NoteArchiveForm
    success_url = '/users/profile'
    template_name_suffix = '_unarchive'
