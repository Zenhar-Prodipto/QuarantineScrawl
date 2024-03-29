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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm

# Create your views here.


def home(request):
    context = {"all_posts": Post.objects.all().order_by[-"created"]}
    return render(request, "blog/home.html", context)


class HomePostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/home.html"
    ordering = ["-date"]
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        loggedInUser = Profile.objects.get(user=self.request.user)

        axeLoggedInUser = Post.objects.exclude(author=loggedInUser.user)
        context["all_posts"] = axeLoggedInUser.exclude(
            author__in=loggedInUser.follow.all()
        ).order_by("-date")
        return context


class AmigosPostListView(LoginRequiredMixin, ListView):

    template_name = "blog/homeWithAmigos.html"

    def get_queryset(self):
        loggedInUser = Profile.objects.get(user=self.request.user)
        axedUser = Post.objects.exclude(author=loggedInUser.user)
        return axedUser.filter(author__in=loggedInUser.follow.all()).order_by("-date")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["all_posts"] = self.get_queryset()
        a = 1
        context["a"] = a
        context["post_comments"] = Comment.objects.filter(post=a)
        return context


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    paginate_by = 8

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

        if viewProfile.user == self.request.user:
            current_user = True
        else:
            current_user = False

        if viewProfile.user in loggedInProfile.follow.all():
            following = True
        else:
            following = False

        if (
            viewProfile.user in loggedInProfile.follow.all()
            and loggedInProfile.user in viewProfile.follow.all()
        ):
            bothFollowing = True
        else:
            bothFollowing = False

        context["following"] = following
        context["all_posts"] = self.get_queryset()
        context["viewProfile"] = Profile.objects.filter(user=viewProfile.user)
        context["comments"] = Comment.objects.filter(post=self.get_queryset())
        context["bothFollowing"] = bothFollowing
        context["current_user"] = current_user

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

        if (
            post_id.author in loggedInProfile.follow.all()
            or post_id.author == loggedInProfile.user
        ):
            displayCommentSection = True
        else:
            displayCommentSection = False

        context["displayReactionButton"] = displayReactionButton
        context["displayCommentSection"] = displayCommentSection
        context["post"] = Post.objects.get(id=post_id.id)
        context["user"] = loggedInProfile.user
        context["comments"] = Comment.objects.filter(post=post_id)
        # context["displayCommentRemoveForm"] = displayCommentRemoveForm
        context["comment_form"] = CommentForm()
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


def CommentRemoveView(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        Comment.objects.filter(id=comment_id).delete()
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


class ProfileVisitView(LoginRequiredMixin, ListView):

    template_name = "blog/visit_profile.html"
    model = Profile

    def get_object(self, **kwargs):  # getting the pk from the url
        usernameFromURL = get_object_or_404(User, username=self.kwargs.get("username"))
        return usernameFromURL

    def top_liked_posts_list(self):
        viewProfile = get_object_or_404(Profile, user=self.get_object())
        viewProfilePosts = Post.objects.filter(author=viewProfile.user)
        top_likes_list = []

        for post in viewProfilePosts:
            top_likes_list.append(post.liked.all().count())

        top = sorted(top_likes_list, reverse=True)[:3]
        return top[:3]

    def number_of_top_post_count(self):
        if len(self.top_liked_posts_list()) == 0:
            no_post = True
            return no_post
        elif len(self.top_liked_posts_list()) == 1:
            one_post = True
            return one_post
        elif len(self.top_liked_posts_list()) == 2:
            two_posts = True
            return two_posts
        elif len(self.top_liked_posts_list()) == 3:
            three_posts = True
            return three_posts
        else:
            return more

    # def top_liked_posts_list(self):
    #     viewProfile = get_object_or_404(Profile, user=self.get_object())
    #     viewProfilePosts = Post.objects.filter(author=viewProfile.user)

    #     top_likes_list = []

    #     for post in viewProfilePosts:
    #         top_likes_list.append(post.liked.all().count())

    #     top = sorted(top_likes_list, reverse=True)
    #     return top[:3]  # first 3 elements

    # def number_of_post_count(self):
    #     top = self.top_liked_posts()
    #     if len(top) == 0:
    #         no_post = True
    #         return no_post
    #     elif len(top) == 1:
    #         one_post = True
    #         return one_post
    #     elif len(top) == 2:
    #         two_posts = True
    #         return two_posts
    #     elif len(top) == 3:
    #         three_posts = True
    #         return three_posts
    #     else:
    #         more = True
    #         return more

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # viewProfile = get_object_or_404(Profile, user=self.get_object())
        viewProfile = Profile.objects.get(user=self.get_object())
        viewProfilePosts = Post.objects.filter(author=viewProfile.user)
        top_likes_list = []

        for post in viewProfilePosts:
            top_likes_list.append(post.liked.all().count())

        top = sorted(top_likes_list, reverse=True)[:3]

        # order_by("-date")[0:3]
        context["top"] = self.top_liked_posts_list()
        context["viewProfile"] = viewProfile
        context["viewProfilePosts"] = viewProfilePosts
        context["top_likes"] = viewProfilePosts.filter(
            liked__in=self.top_liked_posts_list()
        )
        # context["top_likes"]: viewProfilePosts.objects.filter(
        #     liked__in=self.top_liked_posts_list()
        # )
        context["no_post"] = self.number_of_top_post_count()
        context["one_post"] = self.number_of_top_post_count()
        context["two_posts"] = self.number_of_top_post_count()
        context["three_posts"] = self.number_of_top_post_count()
        context["follow_profiles"] = Profile.objects.filter(
            user__in=viewProfile.follow.all()
        )
        context["follower_profiles"] = Profile.objects.filter(
            user__in=viewProfile.follower.all()
        )
        context["list"] = top
        context["ob"] = viewProfilePosts.filter(liked__in=top)

        return context


class VisitProfilefollowingListView(LoginRequiredMixin, ListView):
    template_name = "blog/visit_profile_following_list.html"
    model = Profile

    def no_of_following(self):

        usernameFromURL = get_object_or_404(User, username=self.kwargs.get("username"))
        viewProfile = Profile.objects.get(user=usernameFromURL)
        following_Profiles = Profile.objects.filter(user__in=viewProfile.follow.all())

        if following_Profiles.count == 0:
            no_profile = True
            return no_profile
        elif following_Profiles.count == 1:
            one_profile = True
            return one_profile
        else:
            more_than_one_profile = True
            return more_than_one_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usernameFromURL = get_object_or_404(User, username=self.kwargs.get("username"))
        viewProfile = Profile.objects.get(user=usernameFromURL)
        following_Profiles = Profile.objects.filter(user__in=viewProfile.follow.all())

        context["viewProfile"] = viewProfile
        context["following_Profiles"] = Profile.objects.filter(
            user__in=viewProfile.follow.all()
        )
        context["following_Profile_Posts"] = Post.objects.filter(
            author__in=viewProfile.follow.all()
        )

        for profile in following_Profiles:
            context["f"] = Post.objects.filter(author=profile.user)

        context["no_profile"] = self.no_of_following()
        context["one_profile"] = self.no_of_following()
        context["more_than_one_profile"] = self.no_of_following()

        return context


class VisitProfilefollowerListView(LoginRequiredMixin, ListView):
    template_name = "blog/visit_profile_follower_list.html"
    model = Profile

    def no_of_followers(self):
        usernameFromURL = get_object_or_404(User, username=self.kwargs.get("username"))
        viewProfile = Profile.objects.get(user=usernameFromURL)
        follower_Profiles = Profile.objects.filter(user__in=viewProfile.follower.all())

        if follower_Profiles.count == 0:
            no_profile = True
            return no_profile
        elif follower_Profiles.count == 1:
            one_profile = True
            return one_profile
        else:
            more_than_one_profile = True
            return more_than_one_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usernameFromURL = get_object_or_404(User, username=self.kwargs.get("username"))
        viewProfile = Profile.objects.get(user=usernameFromURL)
        follower_Profiles = Profile.objects.filter(user__in=viewProfile.follower.all())

        context["viewProfile"] = viewProfile
        context["follower_Profiles"] = Profile.objects.filter(
            user__in=viewProfile.follower.all()
        )
        context["follower_Profile_Posts"] = Post.objects.filter(
            author__in=viewProfile.follower.all()
        )

        context["no_profile"] = self.no_of_followers()
        context["one_profile"] = self.no_of_followers()
        context["more_than_one_profile"] = self.no_of_followers()
        context["s"] = follower_Profiles.count

        return context


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