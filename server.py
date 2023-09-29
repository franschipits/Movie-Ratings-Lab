"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """"View homepage"""

    return render_template('homepage.html')


@app.route("/movies")
def all_movies():
    """View all movies"""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """"Show details on a particular movie"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def all_users():
    """"View all users"""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """"Create a new user"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again")
    
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """"Show details on a particular user"""""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def user_login():

    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_email(email)

    if not user:
        flash("Login incorrect")

    elif password != user.password:
        flash("Password incorrect")

    else:
        session['current_user'] = user.email
        flash("Logged in!")

    return redirect("/")
        

@app.route("/rating", methods=["POST"])
def user_rating():

    user = crud.get_user_by_email(session["current_user"])
    movie = request.form.get('movie')
    score = request.form.get('rating')

    
    if user:
        
        rating = crud.create_rating(user, movie, score)
        session['user_rating'] = rating
        db.session.add(rating)
        db.session.commit()

    return redirect("/movies")

#use the movie id 
#whats the score (from the form)
#who is logged in
#print("This is the movie id I got from the HTML form")
#print(movie_id)
#print(type(movie_id))

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
