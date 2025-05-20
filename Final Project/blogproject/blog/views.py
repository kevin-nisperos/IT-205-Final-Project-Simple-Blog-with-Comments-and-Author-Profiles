from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib.auth.models import User

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Post.objects.create(title=title, content=content, author=request.user)
        return redirect('index')
    return render(request, 'blog/create_post.html')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(post=post, commenter=request.user, content=content)
        return redirect('post_detail', post_id=post.id)
    return redirect('post_detail', post_id=post.id)

def author_profile(request, user_id):
    author = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=author)
    return render(request, 'blog/author_profile.html', {'author': author, 'posts': posts})
