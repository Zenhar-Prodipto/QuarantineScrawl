from django.urls import path, include
from .views import (
    HomePostListView,
    PostDetailedView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    AmigosPostListView,
    PostLikeView,
    Test,
    TestDetailed,
    follow_unfollow_view,
    TestAmigos,
    # testView,
)
from . import views

urlpatterns = [
    # class based view teh as_view() laagbe
    path("", HomePostListView.as_view(), name="home"),
    path("homewithamigos/", AmigosPostListView.as_view(), name="amigos-home"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailedView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post/like", views.PostLikeView, name="like-post"),
    path("about/", views.about, name="about"),
    # practice
    # path("testHome/", views.testView, name="test-view"),
    # path("testHome/", testView.as_view(), name="test-view"),
    path("test", Test.as_view(), name="test"),
    path("user/test/<int:pk>", TestDetailed.as_view(), name="test-details"),
    path("user/fu/", views.follow_unfollow_view, name="follow-unfollow-view"),
    path("amigos/", TestAmigos.as_view(), name="test-amigos"),
]
