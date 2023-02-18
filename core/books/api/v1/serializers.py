import json
import urllib

from django.conf import settings
from rest_framework import serializers

from ...models import Book, Author, Category


class BookSerializer(serializers.ModelSerializer):
    details_url = serializers.SerializerMethodField(method_name="get_autor_url")
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    authors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all()
    )
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    isbn = serializers.CharField()

    class Meta:
        model = Book
        fields = [
            "isbn",
            "id",
            "title",
            "authors",
            "subtitle",
            "categories",
            "description",
            "details_url",
            "creator",
            "custom",
        ]

    def validate_isbn(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("ISBN must be an Number")
        return value

    def validate(self, value):
        isbn = value.get("isbn")
        custom = value.get("custom")

        authors_pk = []
        categories_pk = []

        if not custom:
            if len(value.get("isbn")) < 10:
                raise serializers.ValidationError(
                    "Standard ISBN is 10 or 13 character."
                )

            try:
                base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
                with urllib.request.urlopen(base_api_link + str(isbn)) as f:
                    text = f.read()
                decoded_text = text.decode("utf-8")
                obj = json.loads(decoded_text)
                volume_info = obj["items"][0]
                value["title"] = (
                    value.get("title")
                    if value.get("title")
                    else volume_info["volumeInfo"]["title"]
                )
                value["subtitle"] = (
                    value.get("subtitle")
                    if value.get("subtitle")
                    else volume_info["volumeInfo"]["subtitle"]
                )
                value["description"] = (
                    value.get("description")
                    if value.get("subtitle")
                    else volume_info["volumeInfo"]["description"]
                )

                if len(volume_info["volumeInfo"]["authors"]) > 0:
                    for each in volume_info["volumeInfo"]["authors"]:
                        try:
                            pk = Author.objects.get(name=each).pk
                            authors_pk.append(pk)
                        except Exception as e:
                            print("An error occurred: {}".format(str(e)))

                            a = Author(name=each)
                            a.save()
                            authors_pk.append(a.pk)
                    value["authors"] = authors_pk
                if len(volume_info["volumeInfo"]["categories"]) > 0:
                    for each in volume_info["volumeInfo"]["categories"]:
                        try:
                            pk = Category.objects.get(name=each).pk
                            categories_pk.append(pk)
                        except Exception as e:
                            print("An error occurred: {}".format(str(e)))

                            c = Category(name=each)
                            c.save()
                            categories_pk.append(c.pk)
                    value["categories"] = categories_pk
                return value
            except Exception as e:
                print("An error occurred: {}".format(str(e)))
                raise serializers.ValidationError(
                    "ISBN is not valid | enter your custom ISBN and insert fields ( title is important"
                )
        else:
            if len(value.get("title")) == 0:
                raise serializers.ValidationError("Title must be field")
            if len(isbn) > 5:
                raise serializers.ValidationError("Custom ISBN <= 5 character")

            return value

    def get_autor_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        rep["authors"] = [
            AuthorSerializer(related).data for related in instance.authors.all()
        ]
        rep["categories"] = [
            CategorySerializer(related).data for related in instance.categories.all()
        ]
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("details_url")
        return rep


class AuthorSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ["id", "name", "url"]

    def get_url(self, obj):
        return f"{settings.DEFAULT_DOMAIN}/api/v1/author/{obj.pk}/"

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if (
                hasattr(request, "parser_context")
                and request.parser_context is not None
                and request.parser_context.get("kwargs").get("pk")
        ):
            rep.pop("url", None)
        pass
        return rep


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return f"{settings.DEFAULT_DOMAIN}/api/v1/category/{obj.pk}"

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if (
                hasattr(request, "parser_context")
                and request.parser_context is not None
                and request.parser_context.get("kwargs").get("pk")
        ):
            rep.pop("url", None)
        pass
        return rep

    class Meta:
        model = Category
        fields = [
            "name",
            "url",
        ]
