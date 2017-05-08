"""NotesDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.utils.functional import curry
from django.views.defaults import *
from rest_framework_jwt.views import obtain_jwt_token

handler500 = curry(server_error, template_name='500.html')
handler404 = curry(page_not_found, template_name="404.html")
handler403 = curry(permission_denied, template_name='403.html')


urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/notes/', include('notes.api.urls', namespace='notes_api')),
    url(r'^', include('notes.urls', namespace='notes')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^api/users/', include('users.api.urls', namespace='users_api')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/token/auth/', obtain_jwt_token),
]



