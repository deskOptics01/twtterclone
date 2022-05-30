from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Postform
from .models import Post

# Create your views here.


def index(request):
    # If the method is POST
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        # If the form is valid
        if form.is_valid():
            # yes save
            form.save()

            # redirect to home
            return HttpResponseRedirect('/')
        else:
            # no show error
            return HttpResponseRedirect(form.errors.as_json)

    posts = Post.objects.all().order_by('-created_at')[:20]
    form = Postform()

    return render(request, 'posts.html',
                  {'posts': posts})


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')


def edit(request, post_id):
    if request.method == "GET":
        posts = Post.objects.get(id=post_id)
        return render(request, "edit.html", {"posts": posts})
    if request.method == "POST":
        editposts = Post.objects.get(id=post_id)
        form = Postform(request.POST, request.FILES, instance=editposts)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect(form.errors.as_json)


def LikeView(request, post_id):
    new_value = Post.objects.get(id=post_id)
    new_value.likes += 1
    new_value.save()
    return HttpResponseRedirect('/')
