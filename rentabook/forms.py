from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django.contrib.auth.models import User
from .views import BookInstance
from .utils import get_messaged_users


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=32, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EditBookForm(ModelForm):

    # Clean due back field when new status = On loan
    def clean_due_back(self):
       due_back = self.cleaned_data['due_back']
       status = self.cleaned_data['status']
       
       if status == 'o':
           # Check if a date is not in the past.
           if due_back < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

            # Check if a date is in the allowed range (+4 weeks from today).
            if due_back > datetime.date.today() + datetime.timedelta(weeks=4):
                raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return due_back

    class Meta:
        model = BookInstance
        fields = ['borrower', 'status', 'due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')} 

    # Wanting to filter messaged users only
    def __init__(self, user, *args, **kwargs):
        super(EditBookForm, self).__init__(*args, **kwargs)
        self.fields['borrower'].queryset = User.objects.filter(username__in=get_messaged_users(user))
    


class AddBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['cover', 'title', 'author', 'genre', 'summary', 'condition', 'price']
        