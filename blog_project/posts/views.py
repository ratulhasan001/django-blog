from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from . import forms
from . import models


def post_detail(request, id):
    post = get_object_or_404(models.Post.objects.select_related('author'), pk=id)
    return render(request, 'post_detail.html', {'post': post})


@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save()
            messages.success(request, f'Post "{post.title}" was published.')
            return redirect('post_detail', id=post.id)
    else:
        post_form = forms.PostForm()
    return render(request, 'add_post.html', {'form': post_form, 'title': 'Add a post'})


@login_required
def edit_post(request, id):
    post = get_object_or_404(models.Post, pk=id)
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, f'Post "{post.title}" was updated.')
            return redirect('post_detail', id=post.id)
    else:
        post_form = forms.PostForm(instance=post)
    return render(request, 'add_post.html', {'form': post_form, 'title': 'Edit post', 'post': post})


@login_required
def delete_post(request, id):
    post = get_object_or_404(models.Post, pk=id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f'Post "{post.title}" was deleted.')
        return redirect('homepage')
    # A GET request only shows a confirmation page; nothing is deleted.
    return render(request, 'delete_post.html', {'post': post})
