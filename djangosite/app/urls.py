from django.conf.urls import url
from . import views
# hello danny

urlpatterns = [
    url(r'moments_input', views.moments_input),
    url(r'', views.welcome),
]
