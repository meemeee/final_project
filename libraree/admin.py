from django.contrib import admin
from .models import Genre, Book, BookInstance

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookInstance)
