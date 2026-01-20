from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_TEXT = 'текст комментария'
    NOTE_TITLE = 'Заголовок заметки'
    NOTE_SLUG = 'NoteSlug'

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add',)
        # Создаём пользователя и клиент, логинимся в клиенте.
        cls.user = User.objects.create(username='Пользователь')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'text': cls.NOTE_TEXT, 
            'title': cls.NOTE_TITLE,
            'slug': cls.NOTE_SLUG
            }

    def test_anonymous_user_cant_create_note(self):  
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.slug, self.NOTE_SLUG)   
        self.assertEqual(note.author, self.user)