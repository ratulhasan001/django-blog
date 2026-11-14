from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from author.models import Author
from categories.models import Category
from profiles.models import Profile

from .models import Post


class BlogTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('editor', password='pass12345!')
        cls.author = Author.objects.create(name='Ada', bio='Writes things', phone_no='123')
        cls.django = Category.objects.create(name='Django')
        cls.python = Category.objects.create(name='Python')
        cls.post = Post.objects.create(title='Hello Django', content='First post body', author=cls.author)
        cls.post.category.add(cls.django)
        cls.other = Post.objects.create(title='Snakes', content='About Python', author=cls.author)
        cls.other.category.add(cls.python)

    def login(self):
        self.client.login(username='editor', password='pass12345!')


class PublicPagesTests(BlogTestCase):
    def test_home_lists_posts(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello Django')
        self.assertContains(response, 'Snakes')
        # Anonymous visitors do not see edit or delete buttons.
        self.assertNotContains(response, reverse('delete_post', args=[self.post.id]))

    def test_home_empty_state(self):
        Post.objects.all().delete()
        response = self.client.get(reverse('homepage'))
        self.assertContains(response, 'No posts yet')

    def test_filter_by_category(self):
        response = self.client.get(reverse('homepage'), {'category': self.python.id})
        self.assertContains(response, 'Snakes')
        self.assertNotContains(response, 'Hello Django')

    def test_unknown_category_shows_all_posts(self):
        response = self.client.get(reverse('homepage'), {'category': 'abc'})
        self.assertEqual(len(response.context['data']), 2)

    def test_search(self):
        response = self.client.get(reverse('homepage'), {'q': 'python'})
        self.assertEqual(list(response.context['data']), [self.other])
        response = self.client.get(reverse('homepage'), {'q': 'nothing-matches'})
        self.assertContains(response, 'No posts match')

    def test_post_detail(self):
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertContains(response, 'First post body')
        self.assertContains(response, '<title>Hello Django | Django Blog</title>', html=False)

    def test_missing_post_returns_404(self):
        self.assertEqual(self.client.get(reverse('post_detail', args=[999])).status_code, 404)

    def test_login_page_renders(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)


class AnonymousAccessTests(BlogTestCase):
    def test_write_pages_redirect_to_login(self):
        urls = [
            reverse('add_post'),
            reverse('edit_post', args=[self.post.id]),
            reverse('delete_post', args=[self.post.id]),
            reverse('add_author'),
            reverse('add_profile'),
            reverse('add_category'),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_anonymous_cannot_create_post(self):
        self.client.post(reverse('add_post'), {
            'title': 'Spam', 'content': 'x', 'author': self.author.id, 'category': [self.django.id],
        })
        self.assertFalse(Post.objects.filter(title='Spam').exists())

    def test_anonymous_cannot_delete_post(self):
        self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertTrue(Post.objects.filter(pk=self.post.id).exists())


class EditorTests(BlogTestCase):
    def setUp(self):
        self.login()

    def test_create_post(self):
        response = self.client.post(reverse('add_post'), {
            'title': 'New post',
            'content': 'Body',
            'author': self.author.id,
            'category': [self.django.id, self.python.id],
        }, follow=True)
        post = Post.objects.get(title='New post')
        self.assertRedirects(response, reverse('post_detail', args=[post.id]))
        self.assertEqual(post.category.count(), 2)
        self.assertContains(response, 'was published')

    def test_invalid_post_shows_errors(self):
        response = self.client.post(reverse('add_post'), {'title': '', 'content': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertContains(response, 'This field is required')

    def test_edit_post(self):
        response = self.client.post(reverse('edit_post', args=[self.post.id]), {
            'title': 'Renamed',
            'content': 'Changed',
            'author': self.author.id,
            'category': [self.python.id],
        })
        self.assertRedirects(response, reverse('post_detail', args=[self.post.id]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Renamed')
        self.assertEqual(list(self.post.category.all()), [self.python])

    def test_edit_missing_post_returns_404(self):
        self.assertEqual(self.client.get(reverse('edit_post', args=[999])).status_code, 404)

    def test_delete_requires_post_request(self):
        response = self.client.get(reverse('delete_post', args=[self.post.id]))
        self.assertContains(response, 'Are you sure')
        self.assertTrue(Post.objects.filter(pk=self.post.id).exists())

        response = self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertRedirects(response, reverse('homepage'))
        self.assertFalse(Post.objects.filter(pk=self.post.id).exists())

    def test_add_author_category_and_profile(self):
        self.client.post(reverse('add_author'), {'name': 'Grace', 'bio': 'b', 'phone_no': '1'})
        grace = Author.objects.get(name='Grace')
        self.client.post(reverse('add_category'), {'name': 'News'})
        self.assertTrue(Category.objects.filter(name='News').exists())
        self.client.post(reverse('add_profile'), {'name': 'Grace H', 'about': 'a', 'author': grace.id})
        self.assertEqual(Profile.objects.get(author=grace).name, 'Grace H')

    def test_logout_is_post_only(self):
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 302)
