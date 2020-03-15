# Rent-a-book

## Table of contents
* [Description](#description)
* [Installation](#installation)
* [Technologies](#technologies)

## Description

This project is a web application for a book-renting platform that allows book owners to rent out their books independently. Built with Django framework and utilised [django-private-chat](https://github.com/Bearle/django-private-chat) for one-to-one Websocket-based Asyncio-handled chat function.

This is a final project for [CS50Web](https://cs50.harvard.edu/web/).

### Features
- Borrower can browse and search available books, see their details and loan status. 
- Any user can message Loaner via a Websocket-based chat function, where they send borrow requests, or exchange further details such as pick-up time and location.
- Book Loaner can message the Borrower, change their book's status, or remove a book completely from their library.
- Any user can add a new book for loan and become a Loaner.

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
* [Handlebars](https://handlebarsjs.com/guide/) -  Templating language
* [AOS](https://michalsnik.github.io/aos/) - Animate on scroll library
* [Parallax.js](https://pixelcog.github.io/parallax.js/) -  Parallax scrolling effect