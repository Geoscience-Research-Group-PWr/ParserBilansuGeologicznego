from django.urls import path
from . import views
urlpatterns=[path("",views.menu,name="menu"),
             path("type_search/results",views.results,name="results_t"),
             path("name_search/results",views.results,name="results_n"),
             path("name_search",views.name_search,name="name_search"),
             path("type_search",views.type_search,name="type_search"),
             path("type_search/",views.type_search,name="ts1"),
             path("name_search/",views.name_search,name="ns1")]