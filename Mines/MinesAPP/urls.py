from django.urls import path
from . import views
urlpatterns=[path("",views.add,name="index"),path("output",views.add,name="output") ]