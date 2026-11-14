# Django Blog

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)

A small multi-app blog built with Django. Authors, author profiles, categories and posts each live in their own app, and posts are linked to an author (many-to-one) and to any number of categories (many-to-many). The project demonstrates splitting a Django site into apps, modelling relational data with `ForeignKey`, `OneToOneField` and `ManyToManyField`, and building create/edit/delete flows with `ModelForm`s rendered through django-crispy-forms.

## Features

- Four Django apps: `author`, `profiles`, `categories` and `posts`
- Data model: `Author`, `Profile` (one-to-one with `Author`), `Category`, and `Post` (foreign key to `Author`, many-to-many with `Category`)
- Forms to add authors, profiles, categories and posts, rendered with Bootstrap 5 styling via crispy-forms
- Home page that lists every post as a card with a content preview, the author's name and category tags
- Edit and delete actions for posts
- All models registered in the Django admin

| URL | Page |
| --- | --- |
| `/` | All posts |
| `/post/add/` | Add a post |
| `/post/edit/<id>` | Edit a post |
| `/author/add/` | Add an author |
| `/profile/add/` | Add an author profile |
| `/category/add/` | Add a category |
| `/admin/` | Django admin |

## Tech stack

| | |
| --- | --- |
| Language | Python 3.10+ |
| Framework | Django 5.0 |
| Database | SQLite |
| Forms | django-crispy-forms with crispy-bootstrap5 |
| Front end | Django templates, Bootstrap 5.3 (CDN) |

## Project structure

```
django-blog/
├── requirements.txt
└── blog_project/
    ├── manage.py
    ├── blog_project/   # settings, root URLconf, home view
    ├── author/         # Author model and form
    ├── profiles/       # Profile model (one-to-one with Author)
    ├── categories/     # Category model and form
    ├── posts/          # Post model; add, edit and delete views
    └── templates/      # base.html, home.html
```

## Getting started

```bash
git clone https://github.com/ratulhasan001/django-blog.git
cd django-blog

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd blog_project
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/. Run the `manage.py` commands from inside `blog_project/`, because the template directory is configured as a relative path. No environment variables are required.

## Author

Ratul Hasan · [ratulhasan.dev](https://ratulhasan.dev)
