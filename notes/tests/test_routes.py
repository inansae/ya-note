# news/tests/test_routes.py
from http import HTTPStatus

# Импортируем функцию для определения модели пользователя.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Импортируем класс комментария.
from notes.models import Note

# Получаем модель пользователя.
User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='ФИО автора')
        cls.reader = User.objects.create(username='ФИО читателя')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='testing')


    def test_pages_availability_unauthorised(self):
        urls = (
            ('notes:home', None, HTTPStatus.OK),
            ('notes:detail', (self.notes.slug,), HTTPStatus.FOUND),
            ('notes:add', None, HTTPStatus.FOUND),
            ('users:login', None, HTTPStatus.OK),
            ('users:signup', None, HTTPStatus.OK),
        )
        for name, args, http_status in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, http_status)


    def test_availability_authorised(self):
        users = (self.author, self.reader)
        pages = ('notes:list', 'notes:add', 'notes:success')
        for user in users:
            self.client.force_login(user)
            for page in pages:
                with self.subTest(user=user, name=page):        
                    url = reverse(page)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_availability_note_detail(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),            
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:delete', 'notes:detail'):  
                with self.subTest(user=user, name=name):        
                    url = reverse(name, args=(self.notes.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)


    def test_redirect_for_anonymous_client(self):

        login_url = reverse('users:login')
        urls = (
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:detail', (self.notes.slug,)),
            ('notes:delete', (self.notes.slug,)),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
