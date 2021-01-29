from django.shortcuts import render, redirect
from django.contrib.auth.models import User
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
    if request.method == "POST":

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"successfully updated")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)


class UpdatePassword(LoginRequiredMixin, PasswordChangeView, PasswordChangeForm):
    template_name = "users/UserPasswordReset.html"
    success_url = reverse_lazy("profile")


class UpdatePasswordDone(LoginRequiredMixin, PasswordResetDoneView):
    template_name = "users/UserPasswordResetDone.html"
