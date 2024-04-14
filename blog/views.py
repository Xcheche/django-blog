# blog/views.py
from django.http import HttpResponseRedirect
from blog.forms import CommentForm
from django.shortcuts import render
from blog.models import Post, Comment


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    # Retrieve the post object
    post = Post.objects.get(pk=pk)
    
    # Instantiate an empty comment form
    form = CommentForm()
    
    # If the request method is POST, process the form submission
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a new comment associated with the post
            comment = Comment(
                author=form.cleaned_data["author"],
               
                body=form.cleaned_data["body"],
                post=post,  # Use the retrieved post object here
            )
            comment.save()
            # Redirect back to the current page after successful form submission
            return HttpResponseRedirect(request.path_info)

    # Retrieve all comments associated with the post
    comments = Comment.objects.filter(post=post)
    
    # Prepare the context to pass to the template
    context = {
        "post": post,
        "comments": comments,
        "form": form,  # Use the instantiated form here
    }

    # Render the template with the provided context
    return render(request, "blog/detail.html", context)
