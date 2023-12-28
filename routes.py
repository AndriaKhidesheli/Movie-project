from flask import render_template, Flask, redirect, flash, url_for, request, jsonify
from os import path
from forms import AddMovie, RegisterForm, LoginForm, Addseries
from ext import app, db, login_manager
from models import Movies, User, Series, Rating, SeriesRating, Comment, SeriesComment
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/add_series", methods=["POST", "GET"])
@login_required
def add_series_form():
    if current_user.role != "admin":
        return redirect("/")
    form = Addseries()
    if form.validate_on_submit():
        new_series = Series(title=form.name.data, description=form.description.data, img=(form.img.data.filename))
        db.session.add(new_series)
        db.session.commit()

        file_dir = path.join(app.root_path, "static", (form.img.data.filename))
        form.img.data.save(file_dir)
        return redirect("/series")

    return render_template("add_series.html", form=form)


@app.route("/add_movie", methods=["POST", "GET"])
@login_required
def add_movie_form():
    if current_user.role != "admin":
        return redirect("/")

    form = AddMovie()
    if form.validate_on_submit():
        new_movies = Movies(
            title=form.name.data,
            description=form.description.data,
            img=form.img.data.filename,

        )
        db.session.add(new_movies)
        db.session.commit()

        file_dir = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_dir)

        return redirect("/")

    return render_template("add_movie.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")



@app.route("/series_details/<int:series_id>", methods=["GET", "POST"])
def series_details(series_id):
    series = Series.query.get(series_id)

    if request.method == "POST" and current_user.is_authenticated:
        comment_text = request.form.get("comment_text")
        new_comment = SeriesComment(text=comment_text, series_id=series.id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()

    comments = SeriesComment.query.filter_by(series_id=series.id).all()

    return render_template("series_details.html", series=series, comments=comments)


@app.route("/watch_movie/<int:movie_id>", methods=["GET", "POST"])
@login_required
def watch_movie(movie_id):
    movie = Movies.query.get(movie_id)

    if request.method == "POST":
        rating_value = int(request.form.get("rating", 0))
        if 1 <= rating_value <= 5:
            new_rating = Rating(value=rating_value, movie_id=movie.id)
            db.session.add(new_rating)
            db.session.commit()

            return jsonify({"success": True, "average_rating": movie.average_rating})

    return render_template("movie_details.html", movie=movie)

@app.route("/watch_series/<int:series_id>", methods=["GET", "POST"])
@login_required
def watch_series(series_id):
    series = Series.query.get(series_id)

    if request.method == "POST":
        rating_value = int(request.form.get("rating", 0))
        if 1 <= rating_value <= 5:
            new_rating = SeriesRating(series_id=series_id, rating=rating_value)
            db.session.add(new_rating)
            db.session.commit()

            return jsonify({"success": True, "average_rating": series.average_rating})

    return render_template("series_details.html", series=series)

@app.route("/movie_details/<int:movie_id>", methods=["GET", "POST"])
def movie_details(movie_id):
    movie = Movies.query.get(movie_id)

    if request.method == "POST" and current_user.is_authenticated:
        comment_text = request.form.get("comment_text")
        new_comment = Comment(text=comment_text, movie_id=movie.id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()

    comments = Comment.query.filter_by(movie_id=movie.id).all()

    return render_template("movie_details.html", movie=movie, comments=comments)


@app.route("/login", methods=["get", "post"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect("/")
        else:
            flash("Password or username are incorrect. Please try again.")

    return render_template("login.html", form=form)


@app.route("/series")
def series():
    genre_filter = request.args.get('genre')
    if genre_filter:
        series = Series.query.filter_by(genre=genre_filter).all()
    else:
        series = Series.query.all()


    genres = set(series.genre for series in Series.query.all())
    return render_template("series.html", series=series, genres=genres)

@app.route("/")
def home():
    genre_filter = request.args.get('genre')
    if genre_filter:
        movies = Movies.query.filter_by(genre=genre_filter).all()
    else:
        movies = Movies.query.all()
    return render_template("index.html", movies=movies)


@app.route("/delete_movie/<int:index>")
def delete_product(index):
    movies = Movies.query.get(index)
    db.session.delete(movies)
    db.session.commit()
    return redirect("/")


@app.route("/delete_series/<int:index>")
@login_required
def delete_series(index):
    series_item = Series.query.get(index)

    if series_item:
        db.session.delete(series_item)
        db.session.commit()

    return redirect("/series")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter(User.username == form.username.data).first():
            flash("User already exists")
        else:
            user = User(username=form.username.data, password=form.password.data)
            user.create()
            flash("User registered successfully!")
            return redirect("/login")
    else:
        if "repeat_password" in form.errors:
            flash("Passwords don't match. Please try again.")

    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
