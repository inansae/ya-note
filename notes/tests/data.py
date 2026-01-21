from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestDataClass(TestCase):

    TITLE = "Заголовок"
    TEXT = "Текст"
    SLUG = "SlugTest"
    SLUG_TWO = "AnotherSlugTest"
    NEW_TITLE = "Новый заголовок"
    NEW_TEXT = "Новый текст"
    TEST_NOTES_COUNT = 2

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username="Автор")
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.author_other = User.objects.create(username="Другой автор")
        cls.author_other_client = Client()
        cls.author_other_client.force_login(cls.author_other)
        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
            author=cls.author,
            slug=cls.SLUG,
        )
        cls.note_other = Note.objects.create(
            title="Заголовок2",
            text="Текст2",
            author=cls.author_other,
            slug=cls.SLUG_TWO,
        )
        cls.form_data = {
            "title": cls.TITLE, "text": cls.TEXT, "slug": cls.SLUG_TWO
        }
        cls.new_form_data = {
            "title": cls.TITLE, "text": cls.TEXT, "slug": cls.SLUG
        }

        cls.another_new_form_data = {
            "title": cls.NEW_TITLE,
            "text": cls.NEW_TEXT,
            "slug": cls.SLUG_TWO,
        }

        cls.new_form_data_without_slug = {
            "title": cls.NEW_TITLE, "text": cls.NEW_TEXT
        }
        cls.homepage_url = reverse("notes:home")
        cls.note_list_url = reverse("notes:list")
        cls.add_note_url = reverse("notes:add")
        cls.edit_note_url = reverse(
            "notes:edit", kwargs={"slug": cls.note.slug}
        )
        cls.delete_note_url = reverse(
            "notes:delete", kwargs={"slug": cls.note.slug}
        )
        cls.detail_note_url = reverse(
            "notes:detail", kwargs={"slug": cls.note.slug}
        )
        cls.login_url = reverse("users:login")
        cls.logout_url = reverse("users:logout")
        cls.signup_url = reverse("users:signup")
        cls.success_url = reverse("notes:success")
