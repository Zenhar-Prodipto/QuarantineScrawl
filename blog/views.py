from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from users.models import Profile, Comment, Like
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.


def home(request):
    context = {"all_posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


class HomePostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/temp.html"
    ordering = ["-date"]
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        loggedInUser = Profile.objects.get(user=self.request.user)
        context["all_posts"] = Post.objects.exclude(author=loggedInUser.user)
        return context


class AmigosPostListView(LoginRequiredMixin, ListView):

    template_name = "blog/followspost.html"
    context_object_name = "all_posts"

    def get_queryset(self):
        loggedInUser = Profile.objects.get(user=self.request.user)
        ex = Post.objects.exclude(author=loggedInUser.user)
        return ex.filter(author__in=loggedInUser.follow.all())


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "all_posts"
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date")


class PostDetailedView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html")


class Test(ListView):
    model = Profile
    template_name = "blog/test1.html"
    context_object_name = "profiles"

    def queryset(self, **kwargs):

        return Profile.objects.all().exclude(user=self.request.user)


class TestDetailed(DeleteView):
    model = Profile
    template_name = "blog/test2.html"

    def get_object(self, **kwargs):  # getting the pk from the url
        pk = self.kwargs.get("pk")
        viewProfile = Profile.objects.get(pk=pk)
        return viewProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        viewProfile = self.get_object()
        loggedInProfile = Profile.objects.get(user=self.request.user)

        if viewProfile.user in loggedInProfile.follow.all():
            following = True
        else:
            following = False

        context["following"] = following
        context["posts"] = Post.objects.filter(author=viewProfile.user).order_by(
            "-date"
        )
        context["name"] = Profile.objects.filter(user=viewProfile.user)
        return context


def follow_unfollow_view(request):
    if request.method == "POST":
        loggedInProfile = Profile.objects.get(user=request.user)
        pk = request.POST.get("profile_pk")
        viewProfile = Profile.objects.get(pk=pk)

        if viewProfile.user in loggedInProfile.follow.all():
            loggedInProfile.follow.remove(viewProfile.user)
        else:
            loggedInProfile.follow.add(viewProfile.user)

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect("blog:test-details")


# def TestAmigos(request):
#     loggedInProfile = Profile.objects.get(user=request.user)
#     profiles = Profile.follow.all()

#     context = {"all_posts": all_posts}


class TestAmigos(LoginRequiredMixin, ListView):

    template_name = "blog/test3.html"
    context_object_name = "all_posts"

    def get_queryset(self):
        loggedInUser = Profile.objects.get(user=self.request.user)
        ex = Post.objects.exclude(author=loggedInUser.user)
        return ex.filter(author__in=loggedInUser.follow.all())


# def testView(request):
#     posts = Post.objects.all()
#     moja = Post.objects.filter(title__contains="test")
#     context = {"posts": posts, "moja": moja}
#     return render(request, "blog/testView.html", context)


# class testView(ListView):
#     model = Post
#     template_name = "blog/testView.html"
#     queryset = Post.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super(ListView, self).get_context_data(**kwargs)
#         context["posts"] = Post.objects.all()
#         return context
