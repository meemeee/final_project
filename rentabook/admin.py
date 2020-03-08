from django.contrib import admin
from .models import *

from django_private_chat.models import Dialog, Message
admin.site.unregister(Dialog)
admin.site.unregister(Message)

class DialogAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'owner', 'opponent')
    list_filter = ('created', 'modified', 'owner', 'opponent')


admin.site.register(Dialog, DialogAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'is_removed',
        'dialog',
        'sender',
        'text',
    )
    list_filter = ('created', 'modified', 'is_removed', 'dialog', 'sender')


admin.site.register(Message, MessageAdmin)

@admin.register(Genre) 
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover_tag', 'author', 'display_genre', 'status', 'created_by',
                    'borrower', 'due_back')

    list_filter = ('status', 'due_back')

    fieldsets = (
        ('Book Information', {
            'fields': ('cover', 'background_color', 'title', 'author',
            'genre', 'summary')
        }),
        ('Price & Condition', {
            'fields': ('condition', 'price')
        }),
        ('Availability', {
            'fields': ('status', 'created_by', 
            'borrower', 'due_back')
        }),
    )
