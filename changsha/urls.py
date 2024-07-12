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
# Declaration
from changshaapp.settings import declaration_getinfos, declaration_getinfos_by_username, declaration_upload, declaration_delete, declaration_edit

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

    path("declaration/getinfos/", declaration_getinfos, name='declaration_getinfos'),
    path("declaration/getinfos/byUsername/", declaration_getinfos_by_username, name='declaration_getinfos_by_username'),
    path("declaration/upload/", declaration_upload, name='declaration_upload'),
    path("declaration/delete/", declaration_delete, name='declaration_delete'),
    path("declaration/edit/", declaration_edit, name='declaration_edit'),

    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
