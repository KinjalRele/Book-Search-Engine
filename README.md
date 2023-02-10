# Book Search Engine

This is a basic web-based book search engine that enables users to look up books and keep track of their favorite books.
It's built using Flask and leverages the Google Books API and SQLAlchemy for book searches and database storage.
The app uses SQLite database stored in the file named "database.db" for storing the selected favorite books. 
The app has the following functionalities:

1. Search for books by entering a query in the search box and hitting the "Search" button. The app will make an API call to Google Books API with the query and retrieve the top 5 search results. 
The title, authors, subtitle and thumbnail link of the books are stored in separate lists.

2. Add books to the "favorite" books by filling in the form fields for title, subtitle, authors, and thumbnail link and hitting the "Add Book" button. The book information will be added to the SQLite database using SQLAlchemy.

3. Delete books from the "favorite" books by entering the title of the book and hitting the "Delete" button. 
The book information will be deleted from the SQLite database using SQLAlchemy.

4. The app also displays the top 5 favorite books in the database by making API calls to Google Books API using the book's volume id. 
The book's title and thumbnail are retrieved and stored in separate lists. These lists are then displayed on the main page of the app.

## Requirements

  1. Flask
  2. Flask-SQLAlchemy
  3. Requests
  
## Code structure

- main.py contains the main Flask application and all the routes.
- templates/ contains the HTML template files.
- database.db is the SQLite database file used to store the favorite books.

## Tech Stack

- HTML
- CSS
- JavaScript
- Python
- Flask(A python web framework)
- SQLAlchemy (a Python SQL toolkit and Object-Relational Mapping (ORM) library)
- SQLite(A database system)  
