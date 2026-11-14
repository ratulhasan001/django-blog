from django.db.models import Q
from django.shortcuts import render

from categories.models import Category
from posts.models import Post


def home(request):
    data = (
        Post.objects.select_related('author')
        .prefetch_related('category')
        .order_by('-id')
    )

    query = request.GET.get('q', '').strip()
    if query:
        data = data.filter(Q(title__icontains=query) | Q(content__icontains=query))

    selected_category = None
    category_id = request.GET.get('category', '')
    if category_id.isdigit():
        selected_category = Category.objects.filter(pk=category_id).first()
        if selected_category:
            data = data.filter(category=selected_category)

    return render(request, 'home.html', {
        'data': data,
        'query': query,
        'categories': Category.objects.order_by('name'),
        'selected_category': selected_category,
    })
