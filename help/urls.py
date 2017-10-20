from django.conf.urls import url
from . import views

app_name='help'

urlpatterns = [
    #match localhost/help/
    url(r'^$', views.help_form, name='helpform'),
	#match localhost/help/request/
	url(r'^request/$', views.complaint, name='complaint'),
	url(r'^/get_help/', views.get_help, name='get_help'),
	url(r'^/(?P<help_id>\d+)$', views.detailhelp, name='detail'),
]