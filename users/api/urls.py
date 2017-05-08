from django.conf.urls import url
from rest_auth.tests.urls import FacebookLogin

from users.api.views import UserCreateAPIView, UserListAPIView, UserLoginAPIView, GoogleLogin

urlpatterns = [
    url(r'^signup/$', UserCreateAPIView.as_view(), name='signup'),
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^google/$', GoogleLogin.as_view(), name='fb_login'),

]
