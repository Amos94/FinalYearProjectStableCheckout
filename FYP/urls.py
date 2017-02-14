"""FYP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from taggy.views import index as index
from taggy.views import about as about
from taggy.views import annotation as annotation
from taggy.views import adjudication as adjudication
from taggy.views import setCreate as setCreate
from taggy.views import successPage as success
from taggy.views import failPage as fail
from taggy.views import editSet as editSet
from taggy.views import deleteSet as deleteSet

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="index"),
    url(r'^about/', about, name="about"),
    url(r'^annotation/', annotation, name="annotation"),
    url(r'^adjudication/', adjudication, name="adjudication"),
    url(r'^set/create/', setCreate, name="create_set"),
    url(r'^set/edit/', editSet, name="edit_set"),
    url(r'^set/delete/', deleteSet, name="delete_set"),
    url(r'success/', success, name="success"),
    url(r'fail/', fail, name="fail")
]
admin.site.site_header = 'T.A.G.G.Y. ADMINISTRATION BOARD'
admin.site.site_title = 'T.A.G.G.Y.'
