from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like, Comment
from users.models import Profile
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm

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

        axeLoggedInUser = Post.objects.exclude(author=loggedInUser.user)
        context["all_posts"] = axeLoggedInUser.exclude(
            author__in=loggedInUser.follow.all()
        )
        return context


class AmigosPostListView(LoginRequiredMixin, ListView):

    template_name = "blog/followspost.html"
    context_object_name = "all_posts"

    def get_queryset(self):
        loggedInUser = Profile.objects.get(user=self.request.user)
        axedUser = Post.objects.exclude(author=loggedInUser.user)
        return axedUser.filter(author__in=loggedInUser.follow.all())


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    paginate_by = 8
    # slug_field = "username"
    # slug_url_kwarg = "username"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date")

    def get_object(self, **kwargs):

        usernameFromURL = get_object_or_404(User, username=self.kwargs.get("username"))
        viewProfile = get_object_or_404(Profile, user=usernameFromURL)
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
        context["all_posts"] = self.get_queryset()
        context["viewProfile"] = Profile.objects.filter(user=viewProfile.user)
        context["comments"] = Comment.objects.filter(post=self.get_queryset())
        return context


class PostDetailedView(LoginRequiredMixin, DetailView):

    model = Post

    def get_object(self, **kwargs):  # getting the pk from the url
        pk = self.kwargs.get("pk")
        post_id = Post.objects.get(id=pk)
        return post_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_id = self.get_object()
        loggedInProfile = Profile.objects.get(user=self.request.user)

        if post_id.author in loggedInProfile.follow.all():
            displayReactionButton = True
        else:
            displayReactionButton = False

        if post_id.author in loggedInProfile.follow.all():
            displayCommentSection = True
        else:
            displayCommentSection = False

        context["displayReactionButton"] = displayReactionButton
        context["displayCommentSection"] = displayCommentSection
        context["post"] = Post.objects.get(id=post_id.id)
        context["user"] = loggedInProfile.user
        context["comments"] = Comment.objects.filter(post=post_id)
        context["comment_form"] = CommentForm()
        # new_comment = self.post(self.request.POST)
        # context["new_comment"] = new_comment
        return context

    # def post(self, request, *args, **kwargs):

    #     comment_form = CommentForm(data=self.request.POST)
    #     if comment_form.is_valid():
    #         post_id = self.get_object()
    #         loggedInProfile = Profile.objects.get(user=self.request.user)
    #         post_id.commented.add(loggedInProfile.user)
    #         new_comment = comment_form.save(commit=False)
    #         new_comment.save()
    #         return new_comment
    #         # return render(request, {"new_comment": new_comment})


def PostLikeView(request):

    if request.method == "POST":
        loggedInProfile = Profile.objects.get(user=request.user)
        p_id = request.POST.get("post_id_from_form")
        post_id = Post.objects.get(id=p_id)

        if loggedInProfile.user in post_id.liked.all():
            post_id.liked.remove(loggedInProfile.user)
        else:
            post_id.liked.add(loggedInProfile.user)

        like, created = Like.objects.get_or_create(
            user=loggedInProfile.user, post_id=post_id.id
        )

        # if not created:
        #     if like.value == "Like":
        #         like.value = "Unlike"
        #     else:
        #         like.value = "Like"

        like.save()
        return redirect(request.META.get("HTTP_REFERER"))
    return redirect("blog:post-detail")


def PostCommentView(request):
    if request.method == "POST":
        loggedInProfile = Profile.objects.get(user=request.user)
        p_id = request.POST.get("post_id_from_form")
        post_id = Post.objects.get(id=p_id)
        u_comment = request.POST.get("user_comment_from_form")
        post_id.commented.add(loggedInProfile.user)
        new_comment = post_id.comment_set.create(
            post=post_id.id, user=loggedInProfile.user, user_comment=u_comment
        )
        return redirect(request.META.get("HTTP_REFERER"))


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
        pk = request.POST.get("view_profile_pk")
        viewProfile = Profile.objects.get(pk=pk)

        if viewProfile.user in loggedInProfile.follow.all():
            loggedInProfile.follow.remove(viewProfile.user)
            viewProfile.follower.remove(loggedInProfile.user)
        else:
            loggedInProfile.follow.add(viewProfile.user)
            viewProfile.follower.add(loggedInProfile.user)

        return redirect(request.META.get("HTTP_REFERER"))

    # return redirect("blog:test-details")


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


# class UserPostListView(ListView):
#     model = Post
#     template_name = "blog/user_posts.html"
#     context_object_name = "all_posts"
#     paginate_by = 8

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get("username"))
#         return Post.objects.filter(author=user).order_by("-date")