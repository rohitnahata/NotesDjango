from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from notes.forms import NoteForm, LabelForm, NoteArchiveForm
from notes.models import Note, Label


class DispatchFunction(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return HttpResponseRedirect(reverse('users:profile'))
        return super(DispatchFunction, self).dispatch(
            request, *args, **kwargs)

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.author == request.user
        return False


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
        queryset_main = Note.objects.filter(id=object.id)
        queryset = queryset_main.filter(author__username=self.request.user)
        if queryset.count() > 0:
            return object
        queryset = queryset_main.filter(public=True).filter(archived=False)
        if queryset.count() > 0:
            return object
        else:
            return None


class ComposeView(generic.CreateView):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_compose_form'

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ComposeView, self).get_context_data(**kwargs)
        context['form'].fields['labels'].queryset = Label.objects.filter(author=self.request.user)
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


class ComposeLabelView(generic.CreateView):
    model = Label
    form_class = LabelForm
    template_name_suffix = '_new_form'
    success_url = '/users/profile'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            queryset = Label.objects.filter(author__username=request.user)
            if queryset.filter(text=form.cleaned_data['text']).exists():
                messages.warning(request, "Label already exists")
                # raise ValidationError("This label already exists")
            else:
                label.author = request.user
                label.save()
                messages.success(request, "Label successfully saved")
            return HttpResponseRedirect(reverse('users:profile'))


class EditView(generic.UpdateView, DispatchFunction):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['form'].fields['labels'].queryset = Label.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.object.id})


class EditLabelView(generic.UpdateView, DispatchFunction):
    model = Label
    form_class = LabelForm
    template_name_suffix = '_update_form'
    success_url = '/users/profile'


class DeleteView(generic.DeleteView, DispatchFunction):
    model = Note
    success_url = '/users/profile'


class DeleteLabelView(generic.DeleteView, DispatchFunction):
    model = Label
    success_url = '/users/profile'


class UnarchiveView(generic.UpdateView, DispatchFunction):
    model = Note
    form_class = NoteArchiveForm
    success_url = '/users/profile'
    template_name_suffix = '_unarchive'
