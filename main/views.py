from .models import Post, Comment
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

# View for displaying recent posts (home page)
class PostListView(ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Post.objects.filter(title__icontains=query).order_by('-date_posted')
        
        return super().get_queryset()

# View for displaying top viewed posts
class TopListView(ListView):
    model = Post
    template_name = 'main/top.html'
    context_object_name = 'posts'
    ordering = ['-views']
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Post.objects.filter(title__icontains=query).order_by('-date_posted')
        
        return super().get_queryset()

# View for listing posts by a specific user
class UserPostListView(ListView):
    model = Post
    template_name = 'main/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Post.objects.filter(author=user).order_by('-date_posted')
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

# Detail view that increments view count
class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views += 1
        post.save()
        return post

# Authenticated post creation view
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Authenticated + ownership-checked post update view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        
        return False
    
# Authenticated + ownership-checked post deletion view
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        
        return False
    
# Toggle agree on a post via AJAX
@login_required
def PostAgreeView(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.agrees.all():
        post.agrees.remove(request.user)

    else:
        post.agrees.add(request.user)
        post.disagrees.remove(request.user)

    return JsonResponse({'agrees': post.total_agrees(), 'disagrees': post.total_disagrees()})

# Toggle disagree on a post via AJAX
@login_required
def PostDisagreeView(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.disagrees.all():
        post.disagrees.remove(request.user)

    else:
        post.disagrees.add(request.user)
        post.agrees.remove(request.user)
        
    return JsonResponse({'agrees': post.total_agrees(), 'disagrees': post.total_disagrees()})

# Submit comment via AJAX
@login_required
def PostCommentView(request, pk):

    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content')

        if content:
            comment = Comment.objects.create(post=post, author=request.user, content=content)
            return JsonResponse({
                'author': comment.author.username,
                'content': comment.content,
                'date_posted': comment.date_posted.strftime('%b %d, %Y, %I:%M %p')
            })
        
    return JsonResponse({'error': 'Invalid request'}, status=400)
