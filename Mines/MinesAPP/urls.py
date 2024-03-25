from django.urls import path
from . import views
urlpatterns=[path("",views.index1,name="index"),path("results",views.results,name="results") ]