from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime, random
from .models import *
from .forms import *
from .utils import new_message_alert


def index(request):
    """View function for home page of site."""

    # Return 6 latest book instances
    new_arrivals1 = BookInstance.objects.order_by('-id').all()[0:3]
    new_arrivals2 = BookInstance.objects.order_by('-id').all()[3:6]
    
    context = {
        'newArrivals1': new_arrivals1,
        'newArrivals2': new_arrivals2,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context) 
    
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Create new user in database
            form.save()

            # Log user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            return redirect('index')
    
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})


class BookInstanceListView(generic.ListView):
    model = BookInstance
    paginate_by = 12
    ordering = 'status', 'id'

    # Add new message alert
    def get_context_data(self, **kwargs):
        context = super(BookInstanceListView, self).get_context_data(**kwargs)
        context["new_message"] = new_message_alert(self.request.user)
        
        return context

class BookInstanceDetailView(generic.DetailView):
    model = BookInstance
    
    # Add new message alert
    def get_context_data(self, **kwargs):

        # Call the base implementation first to get the context
        context = super(BookInstanceDetailView, self).get_context_data(**kwargs)
        context["new_message"] = new_message_alert(self.request.user)

        return context

class BooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='rentabook/my_books.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('-due_back')

    # Add additional data
    def get_context_data(self, **kwargs):

        # Call the base implementation first to get the context
        context = super(BooksByUserListView, self).get_context_data(**kwargs)

        # Add another query to the context
        context['loaned_books'] = BookInstance.objects.filter(created_by=self.request.user).order_by('-due_back')

        # Add new message alert
        context["new_message"] = new_message_alert(self.request.user)
        
        return context

class SearchView(TemplateView):
    template_name = 'search_books.html'

    # Add new message alert
    def get_context_data(self, **kwargs):

        # Call the base implementation first to get the context
        context = super(SearchView, self).get_context_data(**kwargs)
        context["new_message"] = new_message_alert(self.request.user)
        
        return context

class SearchResultsListView(generic.ListView):
    model = BookInstance
    template_name ='search_results.html'

    # Return list of related books
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = BookInstance.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(genre__name__icontains=query)
        ).order_by('status', 'id').distinct()
   
        return object_list

    # Add additional data
    def get_context_data(self, **kwargs):

        # Call the base implementation first to get the context
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context["keyword"] = self.request.GET.get('q')
        context["new_message"] = new_message_alert(self.request.user)
        
        return context
    
@login_required
def edit_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = EditBookForm(request.user, request.POST)

        # Check if the form is valid:
        if form.is_valid():
            book_instance.status = form.cleaned_data['status']
            # Clear due back date and borrower field if book is back to Available
            if form.cleaned_data['status'] != 'o':
                book_instance.due_back = None
                book_instance.borrower = None
            else:
                book_instance.due_back = form.cleaned_data['due_back']   
                book_instance.borrower = form.cleaned_data['borrower'] 
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        current_status = book_instance.status
        form = EditBookForm(request.user, initial={'due_back': proposed_renewal_date,'status': current_status})

    # Add new message alert
    new_message = new_message_alert(request.user)

    context = {
        'new_message': new_message,
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'rentabook/edit_book.html', context)

@login_required
def add_book(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddBookForm(request.POST, request.FILES)

        # Check if the form is valid:
        if form.is_valid():
            new_book_instance = BookInstance()

            new_book_instance.created_by = request.user
            new_book_instance.cover = form.cleaned_data['cover']
            new_book_instance.title = form.cleaned_data['title']
            new_book_instance.author = form.cleaned_data['author']
            new_book_instance.summary = form.cleaned_data['summary']
            new_book_instance.condition = form.cleaned_data['condition']
            new_book_instance.price = form.cleaned_data['price']

            # Assign a random background color:
            background_color = ['#F3F3F3', '#cabe9f', '#ca9e9f', '#a89eb7', '#aa9593', '#5e6264', '#b0b2a1']
            random_number = random.randrange(7)
            new_book_instance.background_color = background_color[random_number]

            # Save instance first before modifying many-to-many field 
            new_book_instance.save()
            new_book_instance.genre.set(form.cleaned_data['genre'])
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-books') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddBookForm()

    # Add new message alert
    new_message = new_message_alert(request.user)

    # List of added books
    added = list(BookInstance.objects.filter(created_by=request.user).values_list('title', flat=True))

    context = {
        'new_message': new_message,
        'form': form,
        'added_books': added,
    } 

    return render(request, 'rentabook/add_book.html', context)


@login_required
def remove_book(request, pk):
    bookinst = BookInstance.objects.get(pk=pk)
    if bookinst: 
        bookinst.delete()
        return HttpResponseRedirect(reverse('my-books'))
    return HttpResponse("Something went wrong.")


        