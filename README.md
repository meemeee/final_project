# Rent-a-book

## Table of contents
* [Description](#description)
* [Installation](#installation)
* [Technologies](#technologies)

## Description

This project is an online platform that allows individuals to provide private book rental service. Borrowers are presented with a wide selection of books from various Lenders, while Lenders are able to manage their books and communicate with Borrowers at their own convenience.

Built with Django framework and utilized django-private-chat library for a Websocket-based chat function. 
A final project made for [CS50Web](https://cs50.harvard.edu/web/).

### Features
- Borrower can browse and search available books, see their details and loan status. 
- Any user can message Lender via a chat function, where they can send borrow requests, exchange further details such as pick-up time and location.
- Book Lender can message the Borrower, change their book's status, or remove a book completely from their library.
- Any user can add a new book for loan and become a Lender.

## Installation

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. Clone the repo
```
git clone https://github.com/meemeee/rentabook.git
```

2. Install requirements
```
pip3 install -r requirements.txt
```

3. Run on local server
```
python3 manage.py runserver
python3 manage.py run_chat_server
```

## Technologies

* [Django](https://docs.djangoproject.com/en/3.0/) - Python Web framework
* [Bootstrap](https://getbootstrap.com/docs/4.0/) - CSS framework
* [AOS](https://michalsnik.github.io/aos/) - Animate on scroll library
* [Parallax.js](https://pixelcog.github.io/parallax.js/) -  Parallax scrolling effect
* [django-private-chat](https://github.com/Bearle/django-private-chat) - Websocket-based chat function