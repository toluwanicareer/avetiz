from django.conf.urls import url
#from .views import mortageList
from . import views

app_name='pmi'
urlpatterns = [
url(r'^$', views.mortageList.as_view(), name='pmilist'),
url(r'^ajax_product_list/$',views.ajax_get_product_list, name='ajax_product_list')
]