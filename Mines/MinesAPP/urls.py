from django.urls import path
from . import views
urlpatterns=[path("",views.index1,name="add"),path("results",views.results,name="results") ]