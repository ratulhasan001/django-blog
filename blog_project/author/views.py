from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms


@login_required
def add_author(request):
    if request.method == 'POST':
        author_form = forms.AuthorForm(request.POST)
        if author_form.is_valid():
            obj = author_form.save()
            messages.success(request, f'Author "{obj}" was added.')
            return redirect('add_author')
    else:
        author_form = forms.AuthorForm()
    return render(request, 'add_author.html', {'form': author_form})
