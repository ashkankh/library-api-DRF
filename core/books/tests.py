from django.test import TestCase
from .models import Book, Author


class BookTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name="BLIZZARD ENTERTAINMENT")
        cls.book = Book.objects.create(isbn="1616558466")

    def test_book_contect(self):
        self.assertEqual(self.book.title, "World of Warcraft Chronicle Volume 2")
        self.assertEqual(self.book.author.name, "BLIZZARD ENTERTAINMENT")
        self.assertEqual(
            self.book.description,
            "Blizzard Entertainment and Dark Horse Books are thrilled to present the next installment of the wildly popular World of Warcraft Chronicle series. Volume 2 will reveal more sought-after details about the game universe's history and mythology. Showcasing lush, all-new artwork from fan favorites such as Peter Lee, Joseph Lacroix, and Alex Horley, this striking tome is sure to please all fans--casual and collector alike.",
        )
        self.assertEqual(self.book.isbn, "1616558466")
