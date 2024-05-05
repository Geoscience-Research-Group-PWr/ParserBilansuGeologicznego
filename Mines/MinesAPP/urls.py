from . import views
from django.urls import path
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='API Documentation')


urlpatterns=[path("",views.menu,name="menu"),
             path("type_search/results",views.results,name="results_t"),
             path("name_search/results",views.results,name="results_n"),
             path("name_search",views.name_search,name="name_search"),
             path("type_search",views.type_search,name="type_search"),
             path("type_search/",views.type_search,name="ts1"),
             path("name_search/",views.name_search,name="ns1"),
             path("county_search",views.area_search,name="county_search"),
             path("county_search/",views.area_search,name="cs1"),
             path("county_search/results", views.results, name="cs2"),
             ]
