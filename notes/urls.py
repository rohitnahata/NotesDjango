from django.conf.urls import url

from . import views

app_name = 'notes'
urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^(?P<pk>[0-9]+)/edit/$', views.EditView.as_view(), name='edit'),

    url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteView.as_view(), name='delete'),

    url(r'^(?P<pk>[0-9]+)/unarchive/$', views.UnarchiveView.as_view(), name='unarchive'),

    url(r'^compose/$', views.ComposeView.as_view(), name='compose'),

    url(r'^newLabel/$', views.ComposeLabelView.as_view(), name='createLabel'),

    url(r'^(?P<pk>[0-9]+)/editLabel/$', views.EditLabelView.as_view(), name='editLabel'),

    url(r'^(?P<pk>[0-9]+)/deleteLabel/$', views.DeleteLabelView.as_view(), name='deleteLabel'),

]
