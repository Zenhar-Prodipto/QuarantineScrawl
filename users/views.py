from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from blog.models import Post, Like, Comment
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    PasswordChangeForm,
    PasswordChangeView,
    PasswordResetDoneView,
    PasswordResetForm,
)

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

# All the messages

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")
            return redirect("home")

    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    # loggedInUser = request.user
    loggedInProfile = Profile.objects.get(user=request.user)
    current_user_all_posts = Post.objects.filter(author=loggedInProfile.user)
    top_likes_list = []

    for post in current_user_all_posts:
        top_likes_list.append(post.liked.all().count())

    top = sorted(top_likes_list, reverse=True)[:3]

    def top_post_count():
        if len(top) == 0:
            no_post = True
            return no_post
        elif len(top) == 1:
            one_post = True
            return one_post
        elif len(top) == 2:
            two_posts = True
            return two_posts
        elif len(top) == 3:
            three_posts = True
            return three_posts
        else:
            return more

    context = {
        "current_user": Profile.objects.filter(user=loggedInProfile.user),
        "current_user_posts": Post.objects.filter(author=loggedInProfile.user),
        "follow_profiles": Profile.objects.filter(
            user__in=loggedInProfile.follow.all()
        ),
        "follower_profiles": Profile.objects.filter(
            user__in=loggedInProfile.follower.all()
        ),
        "top_likes": current_user_all_posts.filter(liked__in=top),
        "no_post": top_post_count(),
        "one_post": top_post_count(),
        "two_posts": top_post_count(),
        "three_posts": top_post_count(),
    }

    return render(request, "users/profile.html", context)


@login_required
def profileUpdateView(request):
    if request.method == "POST":

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"successfully updated")
            return redirect("profile-update")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile_update.html", context)


class followingListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "users/profile_following_list2.html"

    # def get_followers(self):
    #     loggedInProfile = Profile.objects.get(user=self.request.user)
    #     following_users = Profile.objects.filter(user__in=loggedInProfile.follow.all())
    #     for profile in following_users:
    #         if loggedInProfile.user in profile.follow.all():
    #             return True
    #         else:
    #             return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loggedInProfile = Profile.objects.get(user=self.request.user)

        context["loggedInProfile"] = loggedInProfile
        context["following_Profiles"] = Profile.objects.filter(
            user__in=loggedInProfile.follow.all()
        )
        context["following_Profile_Posts"] = Post.objects.filter(
            author__in=loggedInProfile.follow.all()
        )

        return context


class followerListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "users/profile_follower_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loggedInProfile = Profile.objects.get(user=self.request.user)

        context["loggedInProfile"] = loggedInProfile.user
        context["follower_Profiles"] = Profile.objects.filter(
            user__in=loggedInProfile.follower.all()
        )
        context["following_Profiles"] = Profile.objects.filter(
            user__in=loggedInProfile.follow.all()
        )
        context["follower_Profile_Posts"] = Post.objects.filter(
            author__in=loggedInProfile.follower.all()
        )

        return context


@login_required
def remove_friend_view(request):
    if request.method == "POST":
        loggedInProfile = Profile.objects.get(user=request.user)
        pk = request.POST.get("view_profile_pk")
        viewProfile = Profile.objects.get(pk=pk)

        if viewProfile.user in loggedInProfile.follower.all():
            loggedInProfile.follower.remove(viewProfile.user)
            viewProfile.follow.remove(loggedInProfile.user)

        return redirect(request.META.get("HTTP_REFERER"))


class UpdatePassword(LoginRequiredMixin, PasswordChangeView, PasswordChangeForm):
    template_name = "users/UserPasswordReset.html"
    success_url = reverse_lazy("profile")


class UpdatePasswordDone(LoginRequiredMixin, PasswordResetDoneView):
    template_name = "users/UserPasswordResetDone.html"
