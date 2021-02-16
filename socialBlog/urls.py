"""socialBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from users.views import (
    UpdatePassword,
    UpdatePasswordDone,
    followingListView,
    followerListView,
    remove_friend_view,
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("blog.urls")),
        path("register/", user_views.register, name="register"),
        path("profile/", user_views.profile, name="profile"),
        path("profile/update", user_views.profileUpdateView, name="profile-update"),
        path(
            "profile/<str:username>/following/",
            followingListView.as_view(),
            name="profile-following-list",
        ),
        path(
            "profile/<str:username>/followers/",
            followerListView.as_view(),
            name="profile-follower-list",
        ),
        path(
            "user/remove-friend/",
            remove_friend_view,
            name="remove-friend-view",
        ),
        path(
            "login/",
            auth_views.LoginView.as_view(template_name="users/login.html"),
            name="login",
        ),  # class based view
        path(
            "logout/",
            auth_views.LogoutView.as_view(template_name="users/logout.html"),
            name="logout",
        ),  # class based view
        path(
            "password-reset/",
            auth_views.PasswordResetView.as_view(
                template_name="users/password_reset.html"
            ),
            name="password_reset",
        ),
        path(
            "password-reset/done/",
            auth_views.PasswordResetDoneView.as_view(
                template_name="users/password_reset_done.html"
            ),
            name="password_reset_done",
        ),
        path(
            "password-reset-confirm/<uid64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(
                template_name="users/password_reset_confirm.html"
            ),
            name="password_reset_confirm",
        ),
        path(
            "password-reset-complete/",
            auth_views.PasswordResetCompleteView.as_view(
                template_name="users/password_reset_complete.html"
            ),
            name="password_reset_complete",
        ),
        path(
            "user/update/password-reset/",
            UpdatePassword.as_view(),
            name="password-reset",
        ),
        path(
            "user/update/password-reset-done/",
            UpdatePassword.as_view(),
            name="password-reset-done",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

# if settings.DEBUG:
#     urlpatterns+= + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
