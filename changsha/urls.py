"""changsha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Manager
from changshaapp.settings import getinfo, signin, signout, register
# Declarant
from changshaapp.settings import getinfo2, signin2, signout2, register2
# Authentication
from changshaapp.settings import auth_getinfos, auth_upload, auth_edit, getAuthInfoByUsername

from django.views.static import serve
from django.urls import path, re_path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("getinfo/", getinfo, name='getinfo'),
    path("login/", signin, name='login'),
    path("logout/", signout, name='logout'),
    path("register/", register, name='register'),

    path("getinfo2/", getinfo2, name='getinfo2'),
    path("login2/", signin2, name='login2'),
    path("logout2/", signout2, name='logout2'),
    path("register2/", register2, name='register2'),

    path("auth/getinfos/", auth_getinfos, name='auth_getinfos'),
    path("auth/upload/", auth_upload, name='auth_upload'),
    path("auth/editinfos/", auth_edit, name='auth_editinfos'),
    path("auth/getCodeByUsername/", getAuthInfoByUsername, name='auth_getCodeByUsername'),

    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
