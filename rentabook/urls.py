from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookInstanceListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookInstanceDetailView.as_view(), name='book-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('search/', views.SearchView.as_view(), name='book-search'),
    path('search/results/', views.SearchResultsListView.as_view(), name='search-results'),
]

#Add Django site authentication urls (for login, logout, register)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='register'),
]