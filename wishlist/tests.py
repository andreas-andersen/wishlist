from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.testcases import SimpleTestCase
from django.urls import reverse

from .models import Wish


class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class WishTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='test123'
        )

        self.wish = Wish.objects.create(
            title='A Test Wish',
            author=self.user,
            priority=Wish.HIGH_PRIORITY,
            details='Test Details'
        )

    def test_string_representation(self):
        wish = Wish(title='A Sample Title')
        self.assertEqual(str(wish), wish.title)

    def test_wish_contents(self):
        self.assertEqual(f'{self.wish.title}', 'A Test Wish'),
        self.assertEqual(f'{self.wish.author}', 'testuser'),
        self.assertEqual(f'{self.wish.priority}', 'HI'),
        self.assertEqual(f'{self.wish.details}', 'Test Details')

    def test_post_list_view(self):
        response = self.client.get(reverse('wish_list', kwargs={'pk':self.wish.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A Test Wish')
        self.assertTemplateUsed(response, 'wish_list.html')

    def test_post_detail_view(self):
        response = self.client.get('/wish/1/')
        no_response = self.client.get('/wish/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Details')
        self.assertTemplateUsed(response, 'wish_detail.html')

    def test_wish_create_view(self):
        response = self.client.post(reverse('wish_new', kwargs={'author_id': self.user.id}), {
            'title': 'New wish',
            'author': self.user.id,
            'priority': 'HI',
            'details': 'New detail',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wish.objects.last().title, 'New wish')
        self.assertEqual(Wish.objects.last().priority, 'HI')
        self.assertEqual(Wish.objects.last().details, 'New detail')

    def test_wish_update_view(self):
        response = self.client.post(reverse('wish_update', args='1'), {
            'title': 'Updated wish',
            'priority': 'LO',
            'details': 'Updated detail',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wish.objects.last().title, 'Updated wish')
        self.assertEqual(Wish.objects.last().priority, 'LO')
        self.assertEqual(Wish.objects.last().details, 'Updated detail')

    def test_wish_delete_view(self):
        response = self.client.post(reverse('wish_delete', args='1'))
        self.assertEqual(response.status_code, 302)