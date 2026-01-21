from http import HTTPStatus
from pytils.translit import slugify

from notes.models import Note
from notes.tests.data import TestDataClass


class TestLogic(TestDataClass):

    def test_anonymous_user_cant_create_note(self):
        """Анонимеый пользователь не может создать заметку."""
        self.client.post(self.add_note_url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.TEST_NOTES_COUNT)

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        self.author_client.post(self.add_note_url, self.form_data)
        note_count = Note.objects.count()
        new_note = Note.objects.get(slug=self.SLUG_TWO)
        self.assertEqual(note_count, self.TEST_NOTES_COUNT + 1)
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.title, self.TITLE)
        self.assertEqual(new_note.text, self.TEXT)
        self.assertEqual(new_note.slug, self.SLUG_TWO)

    def test_cant_create_duplicate_note_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        note_count = Note.objects.count()
        self.author_client.post(self.add_note_url, data=self.new_form_data)
        result_count = Note.objects.count()
        self.assertEqual(result_count, note_count)

    def test_auto_slug_generation_with_pytils(self):
        """Если при создании заметки не заполнен slug, то он формируется
        автоматически, с помощью функции pytils.translit.slugify.
        """
        url = self.add_note_url
        self.author_client.post(url, data=self.new_form_data_without_slug)
        test_note = Note.objects.get(title=self.NEW_TITLE, author=self.author)
        result_slug = test_note.slug
        slugified_slug = slugify(self.NEW_TITLE)
        self.assertEqual(result_slug, slugified_slug)

    def test_author_can_delete_his_own_note(self):
        """Пользователь может удалять свои заметки."""
        note_count = Note.objects.count()
        response = self.author_client.post(self.delete_note_url)
        self.assertRedirects(response, self.success_url)
        new_count = Note.objects.count()
        self.assertEqual(note_count - 1, new_count)

    def test_author_can_edit_own_note(self):
        """Пользователь может редактировать свои заметки."""
        response = self.author_client.post(
            self.edit_note_url, data=self.another_new_form_data
        )
        note = Note.objects.get(pk=self.note.pk)
        self.assertRedirects(response, self.success_url)
        self.assertEqual(note.text, self.NEW_TEXT)
        self.assertEqual(note.title, self.NEW_TITLE)
        self.assertEqual(note.author, self.note.author)

    def test_author_can_edit_own_note(self):
        """Пользователь может редактировать свои заметки."""
        response = self.author_client.post(
            self.edit_note_url, data=self.another_new_form_data
        )
        self.assertRedirects(response, self.success_url)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.text, self.NEW_TEXT)
        self.assertEqual(note.title, self.NEW_TITLE)
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_delete_another_users_note(self):
        """Пользователь не может удалять чужие заметки."""
        note_count = Note.objects.count()
        response = self.author_other_client.post(self.delete_note_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        new_count = Note.objects.count()
        self.assertEqual(note_count, new_count)

    def test_user_cant_edit_note_of_another_user(self):
        """Пользователь не может редактировать чужие заметки."""
        response = self.author_other_client.post(
            self.edit_note_url, data=self.another_new_form_data
        )
        test_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(test_note.text, self.note.text)
        self.assertEqual(test_note.title, self.note.title)
        self.assertEqual(test_note.author, self.note.author)
        self.assertEqual(test_note.slug, self.note.slug)
