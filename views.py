from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SignUpForm, PostForm, CommentForm, ProfileForm
from .models import Profile, Post, Comment, Like, Follow

def ensure_profile(user):
    Profile.objects.get_or_create(user=user)

def home(request):
    posts = Post.objects.select_related("user").prefetch_related("likes", "comments__user")
    if request.user.is_authenticated:
        followed_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
        posts = posts.filter(Q(user_id__in=followed_ids) | Q(user=request.user) | Q(user__is_superuser=False))
        for post in posts:
            post.user_liked = post.likes.filter(user=request.user).exists()
    return render(request, "social/home.html", {"posts": posts, "post_form": PostForm(), "comment_form": CommentForm()})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        ensure_profile(user)
        login(request, user)
        messages.success(request, "Welcome to WanderWorld!")
        return redirect("home")
    return render(request, "social/signup.html", {"form": form})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your travel story has been shared.")
        else:
            messages.error(request, "Please check your post details.")
    return redirect("home")

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect(request.POST.get("next") or "home")

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect(request.POST.get("next") or "home")

@login_required
def toggle_follow(request, username):
    person = get_object_or_404(User, username=username)
    if person != request.user:
        relation, created = Follow.objects.get_or_create(follower=request.user, following=person)
        if not created:
            relation.delete()
    return redirect("profile", username=username)

def profile_view(request, username):
    person = get_object_or_404(User, username=username)
    ensure_profile(person)
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=person).exists()
    return render(request, "social/profile.html", {
        "person": person,
        "profile": person.profile,
        "posts": person.posts.all(),
        "is_following": is_following,
        "followers_count": person.follower_links.count(),
        "following_count": person.following_links.count(),
    })

@login_required
def edit_profile(request):
    ensure_profile(request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile", username=request.user.username)
    return render(request, "social/edit_profile.html", {"form": form})

def search_view(request):
    query = request.GET.get("q", "").strip()
    people = User.objects.filter(username__icontains=query)[:12] if query else []
    posts = Post.objects.filter(Q(location__icontains=query) | Q(caption__icontains=query))[:20] if query else []
    return render(request, "social/search.html", {"query": query, "people": people, "posts": posts})
