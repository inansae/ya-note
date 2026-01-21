from http import HTTPStatus

from notes.tests.data import TestDataClass


class TestRoutes(TestDataClass):

    def test_homepage(self):
        """Главная страница доступна анонимному пользователю."""
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_edit_and_delete(self):
        """Страницы отдельной заметки, удаления и редактирования заметки
        доступны только автору заметки. Если на эти страницы попытается зайти
        другой пользователь — вернётся ошибка 404.
        """
        user_statuses = (
            (self.author, HTTPStatus.OK),
            (self.author_other, HTTPStatus.NOT_FOUND),
        )
        for user, status in user_statuses:
            self.client.force_login(user)
            for name in (
                self.detail_note_url,
                self.delete_note_url,
                self.edit_note_url,
            ):
                with self.subTest(user=user, name=name):
                    url = name
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_authenticated_user_note_list_accessibility(self):
        """Аутентифицированному пользователю доступна страница со списком
        заметок notes/, страница успешного добавления заметки done/
        страница добавления новой заметки add/.
        """
        for name in (self.add_note_url, self.note_list_url, self.success_url):
            with self.subTest(user=self.author_other):
                url = name
                response = self.author_other_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        """При попытке перейти на страницу списка заметок, страницу успешного
        добавления записи, страницу добавления заметки, отдельной заметки,
        редактирования или удаления заметки анонимный пользователь
        перенаправляется на страницу логина.
        """
        login_url = self.login_url
        for name in (
            self.add_note_url,
            self.detail_note_url,
            self.delete_note_url,
            self.edit_note_url,
            self.note_list_url,
            self.success_url,
        ):
            with self.subTest(name=name):
                url = name
                redirect_url = f"{login_url}?next={url}"
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_auth_pages_available_for_everyone(self):
        """Страницы регистрации пользователей, входа в учётную запись и выхода
        из неё доступны всем пользователям.
        """
        for url in (self.login_url, self.signup_url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
