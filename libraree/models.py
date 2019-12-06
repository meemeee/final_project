from django.db import models

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Book(models.Model):
    """Defining book details """
    cover = models.ImageField(upload_to='images/', blank=True)
    title = models.CharField(max_length=255, help_text='Enter book title')
    author = models.CharField(max_length=255, help_text='Enter book author')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    summary = models.TextField(
        blank=False,
        max_length=1000, 
        help_text='Enter a brief description of the book')
    
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
    price = models.IntegerField(choices=price_choices, default=10)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book"""
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})' 
