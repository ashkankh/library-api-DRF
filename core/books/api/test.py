import json
import urllib
from core.books.models import Author, Category, Book

min = 1735467227
max = 1735467900

for ig in range(min, max):
    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    with urllib.request.urlopen(base_api_link + str(ig)) as f:
        text = f.read()
    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text)
    volume_info = obj["items"][0]
    print("level1")
    authors_pk = []
    categories_pk = []
    title = volume_info["volumeInfo"]["title"]
    subtitle = volume_info["volumeInfo"]["subtitle"]
    description = volume_info["volumeInfo"]["description"]
    if len(volume_info["volumeInfo"]["authors"]) > 0:
        for each in volume_info["volumeInfo"]["authors"]:
            try:
                pk = Author.objects.get(name=each).pk
                authors_pk.append(pk)
            except:
                a = Author(name=each)
                a.save()
                authors_pk.append(a.pk)
    if len(volume_info["volumeInfo"]["categories"]) > 0:
        for each in volume_info["volumeInfo"]["categories"]:
            try:
                pk = Category.objects.get(name=each).pk
                categories_pk.append(pk)
            except NameError:
                c = Category(name=each)
                c.save()
                categories_pk.append(c.pk)
    print("level2")
    b = Book(
        isbn=each,
        title=title,
        categories=categories_pk,
        description=description,
        subtitle=subtitle,
        authors=authors_pk,
    )
    b.save()
