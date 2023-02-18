from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import urllib.request
import json
from django.contrib.auth.models import User
from django.http import request


class Book(models.Model):
    creator = models.ForeignKey(
        User, related_name="book", on_delete=models.SET_NULL, null=True
    )
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=250, blank=True)
    subtitle = models.CharField(max_length=250, blank=True)
    authors = models.ManyToManyField("Author", blank=True, null=True)
    description = models.TextField(
        blank=True,
    )
    categories = models.ManyToManyField("Category", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    custom = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " | " + self.isbn


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, default="Unknown", unique=True)

    def __str__(self):
        return self.name
