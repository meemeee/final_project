from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


from .models import *
from .forms import *


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    
    context = {
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
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
    paginate_by = 10

class BookInstanceDetailView(generic.DetailView):
    model = BookInstance

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='rentabook/my_borrowed.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class SearchView(TemplateView):
    template_name = 'search_books.html'

class SearchResultsListView(generic.ListView):
    model = BookInstance
    template_name ='search_results.html'

    # Return list of related books
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = BookInstance.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        return object_list