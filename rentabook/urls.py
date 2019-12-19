from django.urls import path, include
from . import views

# app_name = 'rentabook'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookInstanceListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookInstanceDetailView.as_view(), name='book-detail'),
    # path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('search/', views.SearchView.as_view(), name='book-search'),
    path('search/results/', views.SearchResultsListView.as_view(), name='search-results'),
    path('mybooks/', views.BooksByUserListView.as_view(), name='my-books'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit-book'),
]

#Add Django site authentication urls (for login, logout, register)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='register'),
]
