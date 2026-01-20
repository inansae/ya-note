

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class NotesListContextAndFormsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='ФИО автора')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='testing')

    def setUp(self):
        self.client.force_login(self.author)

    def test_note_in_object_list(self):
        response = self.client.get(reverse('notes:list'))

        self.assertIn(
            self.note,
            response.context['object_list']
        )
    
    def test_create_page_has_form(self):
        response = self.client.get(reverse('notes:add'))

        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_page_has_form(self):
        response = self.client.get(
            reverse('notes:edit', args=(self.note.slug,))
        )

        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)


class NotesListUserFilterTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.users = [
            User.objects.create_user(username=username)
            for username in ('user1', 'user2')
        ]

        cls.notes = [
            Note.objects.create(
                title=f'Заметка {i} {user.username}',
                text='Текст',
                slug=f'{user.username}-note-{i}',
                author=user
            )
            for user in cls.users
            for i in range(3)
        ]

        cls.user_1_notes = [
            note for note in cls.notes if note.author == cls.users[0]
        ]
        cls.user_2_notes = [
            note for note in cls.notes if note.author == cls.users[1]
        ]


    def test_notes_only_current_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get(reverse('notes:list'))
        object_list = response.context['object_list']

        for note in self.user_1_notes:
            self.assertIn(note, object_list)

        for note in self.user_2_notes:
            self.assertNotIn(note, object_list)
