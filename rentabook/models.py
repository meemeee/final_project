from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe # Required for image display in admin
from django.urls import reverse
from datetime import date

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class BookInstance(models.Model):
    """Model representing a specific copy of a book"""
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="owner")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="borrower")

    cover = models.ImageField(upload_to='images/', blank=False)
    def cover_tag(self):
        if self.cover:
            return mark_safe('<img src="%s" style="width: 45px; height: 60px;" />' % self.cover.url)
        else:
            return 'No Cover Found'
    cover_tag.short_description = 'Cover'

    title = models.CharField(max_length=255, blank=False, help_text='Enter book title')
    author = models.CharField(max_length=255, blank=False, help_text='Enter book author')
    genre = models.ManyToManyField(Genre, blank=False, help_text='Select a genre for this book')
    summary = models.TextField(
        blank=False,
        max_length=1000, 
        help_text='Enter a brief description of the book (max. 1000 characters)')
    background_color = models.CharField(max_length=10, blank=False, help_text='Enter background color')
    condition_choices = [
        ('1', 'Like New'),
        ('2', 'Good'),
        ('3', 'Fair'),
    ]
    condition = models.CharField(
        choices=condition_choices, 
        max_length=1, 
        blank=False, 
        default='p')
    
    price_choices = [(i, i) for i in range (10, 60, 10)]
    price = models.IntegerField(choices=price_choices, default=10, blank=False)

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('m', 'Maintenance'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back', 'status']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.title})'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

    # Tell when book is overdue
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
