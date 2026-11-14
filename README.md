# Django Blog

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)

One of my early Django projects, built in 2024 while I was learning the framework.

A small multi-app blog. Authors, author profiles, categories and posts each live in their own app, and posts are linked to an author (many-to-one) and to any number of categories (many-to-many).

While building it I practised:

- splitting a Django site into several apps
- modelling relational data with `ForeignKey`, `OneToOneField` and `ManyToManyField`
- create, edit and delete flows with `ModelForm`s, rendered through django-crispy-forms
- template inheritance with a shared base template

## Features

- Four Django apps: `author`, `profiles`, `categories` and `posts`
- Data model: `Author`, `Profile` (one-to-one with `Author`), `Category`, and `Post` (foreign key to `Author`, many-to-many with `Category`)
- Home page that lists every post as a card with a content preview, the author's name and category tags
- Search box (title and content) and category filter buttons on the home page
- A page for each post with its full text
- Forms to add authors, profiles, categories and posts, and to edit and delete posts. These need a logged-in user; visitors can only read.
- All models registered in the Django admin

| URL | Page |
| --- | --- |
| `/` | All posts (`?q=` to search, `?category=<id>` to filter) |
| `/post/<id>/` | A single post |
| `/post/add/` | Add a post (login required) |
| `/post/edit/<id>` | Edit a post (login required) |
| `/post/delete/<id>` | Confirm and delete a post (login required) |
| `/author/add/` | Add an author (login required) |
| `/profile/add/` | Add an author profile (login required) |
| `/category/add/` | Add a category (login required) |
| `/accounts/login/` | Log in |
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
    ├── posts/          # Post model; detail, add, edit and delete views, tests
    └── templates/      # base.html, home.html, registration/login.html
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

Then open http://127.0.0.1:8000/ and log in with the superuser account (`/accounts/login/`) to add authors, categories and posts. There is no sign-up page; further accounts can be created in the admin.

No environment variables are required. For anything other than local use, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` and `DJANGO_ALLOWED_HOSTS` (comma-separated).

## Running the tests

```bash
cd blog_project
python manage.py test
```

The tests cover the post list, search and category filter, the post page, the login requirement on every form, and creating, editing and deleting posts.

## Later improvements

The original coursework version was tidied up later. Changes made then:

- Adding, editing and deleting now require a logged-in user (previously anyone could change or delete posts).
- Deleting a post now asks for confirmation and only happens on a POST request; before, simply visiting the delete link removed the post.
- Missing posts return a 404 page instead of a server error.
- The navbar search box, which did nothing, now searches posts. Added category filters and a post page.
- Page titles, an active navbar link, success messages, a footer and empty-state messages.
- The template directory is resolved from the project folder, so `manage.py` works from any directory.
- `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` can be set through environment variables.
- Added a test suite.

## Author

Ratul Hasan · [ratulhasan.dev](https://ratulhasan.dev)
