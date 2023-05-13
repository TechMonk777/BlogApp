from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import CommentForm
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.
all_posts = Post.objects.all()


class IndexPageView(ListView):
    template_name = "index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "latest_posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
# def index(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request,'index.html',{'latest_posts':latest_posts})


class AllPostsView(ListView):
    template_name = "all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


def posts(request):
    return render(request, 'all-posts.html', {"posts": all_posts})


class PostDetailView(View):
    def get(self, request, id):
        filtered_post = Post.objects.get(id=id)
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = filtered_post.id in stored_posts
        else:
            is_saved_for_later = False
        return render(request, 'post-detail.html', {
            "filtered_post": filtered_post,
            "post_tags": filtered_post.tags.all(),
            "comment_form": CommentForm(),
            "comments":filtered_post.comments.all(),
            "is_saved_for_later":is_saved_for_later
        })

    def post(self, request, id):
        comment_form = CommentForm(request.POST)
        filtered_post = Post.objects.get(id=id)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = filtered_post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail", args=[id]))
        
        return render(request, 'post-detail.html', {
            "filtered_post": filtered_post,
            "post_tags": filtered_post.tags.all(),
            "comment_form": CommentForm()
        })


def post_details(request, id):
    # filtered_post = Post.objects.get(id=id)
    # following code handle if we did not get any post back from model
    filtered_post = get_object_or_404(Post, id=id)
    return render(request, 'post-detail.html', {
        "filtered_post": filtered_post,
        "post_tags": filtered_post.tags.all()
    })

class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts)==0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request,"stored-posts.html",context)


    def post(self,request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")
 