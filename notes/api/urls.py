from django.conf.urls import url

from notes.api.views import NoteListAPIView, NoteDetailAPIView, NoteEditAPIView, NoteDeleteAPIView, NoteComposeAPIView

urlpatterns = [
    # ex: /notes or /notes?label=journal
    url(r'^$', NoteListAPIView.as_view(), name='list'),
    # ex: /notes/2
    url(r'^(?P<pk>[0-9]+)/$', NoteDetailAPIView.as_view(), name='detail'),
    # # ex: /notes/2/edit
    url(r'^(?P<pk>[0-9]+)/edit/$', NoteEditAPIView.as_view(), name='edit'),
    # # ex: /notes/2/edit
    url(r'^(?P<pk>[0-9]+)/delete/$', NoteDeleteAPIView.as_view(), name='delete'),
    # # ex: /notes/compose
    url(r'^compose/$', NoteComposeAPIView.as_view(), name='compose'),
]
