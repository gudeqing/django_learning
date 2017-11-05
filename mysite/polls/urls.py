from django.conf.urls import url
#xxx

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
