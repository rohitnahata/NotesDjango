from django.conf.urls import url

from users.api.views import UserCreateAPIView, UserListAPIView, UserLoginAPIView

urlpatterns = [
    url(r'^signup/$', UserCreateAPIView.as_view(), name='signup'),
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),

]
