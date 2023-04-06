from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .models import Post, Group
from .forms import PostForm


User = get_user_model()


POSTS_TO_DISPLAY: int = 10


def index(request):
    post_list = Post.objects.all()

    paginator = Paginator(post_list, POSTS_TO_DISPLAY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    text = "Последние обновления на сайте"

    context = {
        'page_obj': page_obj,
        'text': text
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()

    paginator = Paginator(posts, POSTS_TO_DISPLAY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author__exact=author)
    posts_number = posts.count()

    paginator = Paginator(posts, POSTS_TO_DISPLAY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts_number': posts_number,
        'page_obj': page_obj,
        'author': author,

    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)

        return render(request, 'posts/create_post.html', {'form': form})

    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        redirect(request, 'posts:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(instance=post)
    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'is_edit': True, 'post_id': post.id}
    )
