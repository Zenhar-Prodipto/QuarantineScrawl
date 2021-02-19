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
    PostCommentView,
    Test,
    TestDetailed,
    follow_unfollow_view,
    TestAmigos,
    ProfileVisitView,
    VisitProfilefollowingListView,
    VisitProfilefollowerListView,
    # testView,
)


from . import views

urlpatterns = [
    # class based view teh as_view() laagbe
    path("", HomePostListView.as_view(), name="home"),
    path("homewithamigos/", AmigosPostListView.as_view(), name="amigos-home"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path(
        "user/<str:username>/profile/", ProfileVisitView.as_view(), name="profile-visit"
    ),
    path(
        "visit/profile/<str:username>/following/",
        VisitProfilefollowingListView.as_view(),
        name="visit-profile-following-list",
    ),
    path(
        "visit/profile/<str:username>/follower/",
        VisitProfilefollowerListView.as_view(),
        name="visit-profile-follower-list",
    ),
    path("post/<int:pk>/", PostDetailedView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post/like", views.PostLikeView, name="like-post"),
    path("post/comment", views.PostCommentView, name="comment-post"),
    path("about/", views.about, name="about"),
    path("user/follow-user/", views.follow_unfollow_view, name="follow-unfollow-view"),
    # practice
    # path("testHome/", views.testView, name="test-view"),
    # path("testHome/", testView.as_view(), name="test-view"),
    path("test", Test.as_view(), name="test"),
    path("user/test/<int:pk>", TestDetailed.as_view(), name="test-details"),
    path("amigos/", TestAmigos.as_view(), name="test-amigos"),
]


# from .models import Post, Comment
# from .forms import EmailPostForm, CommentForm

# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post, slug=post,
#                                    status='published',
#                                    publish__year=year,
#                                    publish__month=month,
#                                    publish__day=day)

#     # List of active comments for this post
#     comments = post.comments.filter(active=True)

#     new_comment = None

#     if request.method == 'POST':
#         # A comment was posted
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post,
#                    'comments': comments,
#                    'new_comment': new_comment,
#                    'comment_form': comment_form})


# self.request.user
# self.kwargs.get("username")
# request.get("username")