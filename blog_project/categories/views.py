from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms


@login_required
def add_category(request):
    if request.method == 'POST':
        category_form = forms.CategoryForm(request.POST)
        if category_form.is_valid():
            obj = category_form.save()
            messages.success(request, f'Category "{obj}" was added.')
            return redirect('add_category')
    else:
        category_form = forms.CategoryForm()
    return render(request, 'add_category.html', {'form': category_form})
