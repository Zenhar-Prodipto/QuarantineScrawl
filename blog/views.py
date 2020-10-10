from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
 
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
 
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post  

    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
         
def about(request):
    return render(request,'blog/about.html')
