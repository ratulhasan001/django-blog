from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms


@login_required
def add_profile(request):
    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST)
        if profile_form.is_valid():
            obj = profile_form.save()
            messages.success(request, f'Profile "{obj}" was added.')
            return redirect('add_profile')
    else:
        profile_form = forms.ProfileForm()
    return render(request, 'add_profile.html', {'form': profile_form})
