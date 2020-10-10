from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView

# Create your views here.


def home(request):
    context={
    'all_posts' : Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<appname>/<model>_<viewtype>.html
    context_object_name = 'all_posts' #jei name template e loop korbo
    ordering =['-date']

class PostDetailedView(DetailView):
    model = Post
    template_name = 'blog/home.html' #<appname>/<model>_<viewtype>.html
    context_object_name = 'all_posts' #jei name template e loop korbo
    ordering =['-date']

def about(request):
    return render(request,'blog/about.html')
