import os
from crypt import methods
import flask
import requests
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

API_KEY = os.getenv("API_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))

# Pointing SQLAlchemy to Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) 

class BooksDB(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(240))
        subtitle = db.Column(db.String(240))
        authors = db.Column(db.String(240))
        thumbnailLink = db.Column(db.String(280))

with app.app_context():
        db.create_all()

#Adding books to BooksDB        
@app.route("/create", methods = ["POST"])
def create():
        create_title = flask.request.form.get('add_book_title')
        create_subtitle = flask.request.form.get('add_book_subtitle')
        create_author = flask.request.form.get('add_book_author')
        create_thumbnail = flask.request.form.get('add_book_thumbnail')

        new_book = BooksDB(
                title =  create_title,
                thumbnailLink = create_thumbnail,
                subtitle =  create_subtitle,
                authors = create_author
        )
        db.session.add(new_book)
        db.session.commit()
        return flask.redirect("/")

#Deleting books from BooksDB
@app.route("/delete", methods = ["POST"])
def delete(): 
        bookTitle_to_delete = flask.request.form.get('book_name')
        to_delete = BooksDB.query.filter_by(title = bookTitle_to_delete).first()
        db.session.delete(to_delete)
        db.session.commit()
        return flask.redirect("/")

#Making API calls to get the search results for searched books
@app.route("/")
def index():
        
        form_data = flask.request.args
        query = form_data.get("term" , "")
       
        response = requests.get(
        "https://www.googleapis.com/books/v1/volumes?",
        params={"q": query, "key": API_KEY},        
        )

        response_json = response.json()
        books_found_title= []
        books_found_subtitle =[]
        books_found_authors =[]
        books_found_thumbnails = []
        
        for i in range(0,5):
                try:
                        books_found_title.append(response_json["items"][i]["volumeInfo"]["title"]) 
                except:
                        print("")
                try:
                        books_found_authors.append(response_json["items"][i]["volumeInfo"]["authors"])
                except:
                        print("")
                try:
                        books_found_thumbnails.append(response_json["items"][i]["volumeInfo"]["imageLinks"]["thumbnail"])
                except:
                        print("No Image :(")
                try:
                        books_found_subtitle.append(response_json["items"][i]["volumeInfo"]["subtitle"])
                except:
                        print("no subtitle")
        
        #Top 5 favorite books in the datbase displayed by making API calls using their Volume Ids
        books_volume_ids = ["3IbqPgAACAAJ", "FzVjBgAAQBAJ", "dqRETZRkGCcC", "Eka9DAAAQBAJ", "BvjFAAAAIAAJ"]
        books_list = []
        images_list = []
        for book_id in books_volume_ids:
                response = requests.get(f"https://www.googleapis.com/books/v1/volumes/{book_id}?/{API_KEY}")
                response_json = response.json()
                books_list.append(response_json["volumeInfo"]["title"])
                images_list.append(response_json["volumeInfo"]["imageLinks"]["thumbnail"])

        favorite_books = BooksDB.query.all()
        num_favoriteBooks = len(favorite_books)
        return flask.render_template(
                "index.html",
                favorite_books = favorite_books,
                num_favoriteBooks = num_favoriteBooks,
                books_found_title = books_found_title,
                books_found_subtitle = books_found_subtitle,
                books_found_authors = books_found_authors,
                books_found_thumbnails = books_found_thumbnails
        )

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.run(use_reloader = True, debug = True)  