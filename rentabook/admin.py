from django.contrib import admin
from .models import *

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'created_by')

    inlines = [BooksInstanceInline]

@admin.register(Genre) 
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')

    list_filter = ('status', 'due_back')