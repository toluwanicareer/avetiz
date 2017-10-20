from django.conf.urls import url
from . import views

app_name='home'

urlpatterns = [
 url(r'^$', views.home, name='index'),
 url(r'^recent_listing/$',views.recent, name='recent'),

]