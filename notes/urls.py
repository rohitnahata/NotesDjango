from django.conf.urls import url
from . import views
from django.views import View

app_name = 'notes'
urlpatterns = [
    # ex: /notes or /notes?label=journal
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /notes/2
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /notes/2/edit
    url(r'^(?P<pk>[0-9]+)/edit/$', views.EditView.as_view(), name='edit'),
    # ex: /notes/2/edit
    url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteView.as_view(), name='delete'),
    # ex: /notes/compose
    url(r'^compose/$', views.ComposeView.as_view(), name='compose'),
]
