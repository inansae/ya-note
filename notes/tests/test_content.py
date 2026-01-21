from notes.forms import NoteForm
from notes.tests.data import TestDataClass


class TestContent(TestDataClass):

    def test_note_in_context_object_list(self):
        """Отдельная заметка передаётся на страницу со списком заметок в списке
        object_list в словаре context.
        """
        response = self.author_client.get(self.note_list_url)
        note_list = response.context["object_list"]
        self.assertIn(self.note, note_list)

    def test_notes_list_author_matches(self):
        """В список заметок одного пользователя не попадают заметки другого
        пользователя.
        """
        response = self.author_client.get(self.note_list_url)
        note_list = response.context["object_list"]
        self.assertNotIn(self.note_other, note_list)

    def test_add_edit_pages_forms(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (self.add_note_url, self.edit_note_url)
        for url in urls:
            with self.subTest():
                response = self.author_client.get(url)
                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)
