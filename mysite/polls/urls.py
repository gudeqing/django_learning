from django.conf.urls import url
#xxx
#add_by_gdq

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
