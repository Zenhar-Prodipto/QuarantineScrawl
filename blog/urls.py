from django.urls import path,include
from .views import PostListView
from . import views

urlpatterns = [
    path("",PostListView.as_view(),name="home"), #class based view teh as_view() laagbe
    path("about/",views.about,name='about'),
]
