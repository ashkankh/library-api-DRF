from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import urllib.request
import json


class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(
        max_length=250,
        blank=True
    )
    subtitle = models.CharField(max_length=250, blank=True)
    author = models.ForeignKey("Author", blank=True, on_delete=models.CASCADE)
    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.title + " | " + self.isbn

    def save(self, *args, **kwargs):
        """Override Data"""
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        with urllib.request.urlopen(base_api_link + str(self.isbn)) as f:
            text = f.read()
        decoded_text = text.decode("utf-8")
        obj = json.loads(decoded_text)
        """
        get data from googleapis.com/book
        """
        try:
            """
            if ISBN is valid or exist Code below RUN
            """
            volume_info = obj["items"][0]
            try:
                """
                Auther exist in DataBase
                """
                A = Author.objects.get(name=volume_info["volumeInfo"]["authors"][0])
                self.author = A
            except ObjectDoesNotExist:
                """
                Auther Doesn't in exist DataBase ( Author Object will be create )
                """
                A = Author(name=volume_info["volumeInfo"]["authors"][0])
                A.save()
                self.author = A
            if self.title == "":
                try:
                    self.title = volume_info["volumeInfo"]["title"]
                except:
                    pass
            if self.description == "":
                try:
                    self.description = volume_info["volumeInfo"]["description"]
                except:
                    pass
            if self.subtitle == "":
                try:
                    self.subtitle = volume_info["volumeInfo"]["subtitle"]
                except:
                    pass
            super(Book, self).save(*args, **kwargs)
        except :
            super(Book, self).save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=100, default="Unknown", unique=True)

    def __str__(self):
        return self.name
