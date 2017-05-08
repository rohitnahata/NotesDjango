from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # url(r'^$', views.index, name="index"),

    # ex: /users/signup
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    # ex: /users/login
    url(r'^login/', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    # ex: /users/logout
    url(r'^logout/', auth_views.logout, name='logout'),
    # ex: /users/profile
    url(r'^profile/', views.ProfileView.as_view(), name='profile'),
]
