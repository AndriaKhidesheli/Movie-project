from ext import db, app, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

class SeriesRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    img = db.Column(db.String)
    trailer_url = db.Column(db.String)
    ratings = relationship('Rating', backref='movie', lazy=True)
    genre = db.Column(db.String)

    @property
    def average_rating(self):
        if self.ratings:
            return sum(r.value for r in self.ratings) / len(self.ratings)
        return 0

    def create(self):
        db.session.add(self)
        db.session.commit()

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    img = db.Column(db.String)
    trailer_url = db.Column(db.String)
    ratings = db.relationship('SeriesRating', backref='series', lazy=True)
    genre = db.Column(db.String)

    @property
    def average_rating(self):
        if self.ratings:
            return sum([rating.rating for rating in self.ratings]) / len(self.ratings)
        return 0

    def create(self):
        db.session.add(self)
        db.session.commit()






class SeriesComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('series_comments', lazy=True))
    series = db.relationship('Series', backref=db.backref('comments', lazy=True))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='comments')

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()


def init_db():
    with app.app_context():
        db.create_all()


class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    with app.app_context():
        init_db()

        admin_user = User.query.filter_by(username="admin_user").first()
        if not admin_user:
            admin_user = User(username="admin_user", password="admin001", role="admin")
            admin_user.create()

        normal_user = User.query.filter_by(username="normal_user").first()
        if not normal_user:
            normal_user = User(username="normal_user", password="password", role="guest")
            normal_user.create()

        movies_data = [

            {
                "title": "The Basketball Diaries",
                "description": "Jim Carroll is a high school basketball player growing up in Manhattan...",
                "img": "bas.jpg",
                "genre": "Drama",
                "trailer_url": "https://www.youtube.com/embed/-Zc7T0vUpj0",
            },
            {
                "title": "Mid 90S",
                "description": "In 1990s Los Angeles, a 13-year-old spends his summer navigating between a troubled home life and a crew of new friends he meets at a skater",
                "img": "images.jpg",
                "genre": "Comedy",
                "trailer_url": "https://www.youtube.com/embed/w9Rx6-GaSIE",
            },
            {
                "title": "The Godfather",
                "description": "The Godfather is a trilogy of American crime films directed by Francis Ford Coppola inspired by the 1969 novel of the same name by Italian American author Mario Puzo.",
                "img": "god.jpg",
                "genre": "Action",
                "trailer_url": "https://www.youtube.com/embed/sY1S34973zA",

            },
            {
                "title": "Fight Club",
                "description": "Unhappy with his capitalistic lifestyle, a white-collared insomniac forms an underground fight club with Tyler, a careless soap salesman. Soon, their venture spirals down into something sinister.",
                "img": "fc.jpg",
                "genre": "Action",
                "trailer_url": "https://www.youtube.com/embed/SUXWAEX2jlg",
            },
            {
                "title": "The Hangover",
                "description": "A few days before his wedding, Doug Billings and his best men go to Las Vegas for a bachelor party. However, the next day, the friends realise that they have no recollection of the previous night.",
                "img": "hg.jpg",
                "genre": "Comedy",
                "trailer_url": "https://www.youtube.com/embed/tcdUhdOlz9M",
            },
            {
                "title": "Green Mile",
                "description": "Paul Edgecomb, the head guard of a prison, meets an inmate, John Coffey, a black man who is accused of murdering two girls. His life changes drastically when he discovers that John has a special gift.",
                "img": "images (4).jpg",
                "genre": "Drama",
                "trailer_url": "https://www.youtube.com/embed/Bg7epsq0OIQ",
            },
            {
                "title": "Vacation",
                "description": "Rusty Griswold plans a cross-country road trip with his wife and two sons in a bid to revive the lost ties between them. However, their trip turns into a series of mishaps, leading to altercations.",
                "img": "vac.jpg",
                "genre": "Comedy",
                "trailer_url": "https://www.youtube.com/embed/kleG7XCqOb4",
            },
            {
                "title": "Dumb and Dumber",
                "description": "Dumb and Dumber is a series of comedy films starring Jim Carrey and Jeff Daniels. The films have been released from 1994 to 2014.",
                "img": "dum.jpg",
                "genre": "Comedy",
                "trailer_url": "https://www.youtube.com/embed/l13yPhimE3o",
            },

        ]

        for movie_data in movies_data:
            existing_movie = Movies.query.filter_by(title=movie_data["title"]).first()
            if not existing_movie:
                new_movie = Movies(**movie_data)
                new_movie.create()

        series_data = [
            {
                "title": "Stranger Things",
                "description": "A group of kids in a small town uncover a series of supernatural mysteries and government conspiracies.",
                "img": "strange.jpg",
                "genre": "Action",
                "trailer_url": "https://www.youtube.com/embed/b9EkMc79ZSU",
            },
            {
                "title": "Game of Thrones",
                "description": "Noble families vie for control of the Iron Throne in the mythical land of Westeros.",
                "img": "got.jpg",
                "genre": "Action",
                "trailer_url": "https://www.youtube.com/embed/KPLWWIOCOOQ",
            },
            {
                "title": "looking for alaska",
                "description": "Miles takes admission to a boarding school, where he comes across Alaska Young and eventually falls for her. During the course of their relationship, he realises that she is facing problems.",
                "img": "alas.jpg",
                "genre": "Drama",
                "trailer_url": "https://www.youtube.com/embed/7tqex95uXY8" ,
            },
            {
                "title": "Prison Break",
                "description": "Michael Scofield finds himself in the Ogygia Prison in Sana'a, Yemen, seven years after his apparent death. His friends, brother and fellow escapee do everything it takes to bring him home.",
                "img": "prison.jpg",
                "genre": "Action",
                "trailer_url": "https://www.youtube.com/embed/AL9zLctDJaU",
            },
            {
                "title": "The Mentalist",
                "description": "Using his heightened observational skills and impeccable knowledge of the human psyche, a consultant helps solve several criminal cases in search of his family's killer.",
                "img": "ment.jpg",
                "genre": "Drama",
                "trailer_url": "https://www.youtube.com/embed/nn2Q69pSC_M",
            },
            {
                "title": "The 100",
                "description": "A nuclear conflict has decimated civilisation. A century later, a spaceship accommodating humanity's lone survivors dispatch 100 juvenile delinquents back to the Earth to determine its habitability.",
                "img": "the.jpg",
                "genre": "Drama",
                "trailer_url": "https://www.youtube.com/embed/ia1Fbg96vL0",
            },
            {
                "title": "Squid Gmae",
                "description": "Hundreds of cash-strapped contestants accept an invitation to compete in children's games for a tempting prize, but the stakes are deadly.",
                "img": "sq.jpg",
                "genre": "Thriller",
                "trailer_url": "https://www.youtube.com/embed/oqxAJKy0ii4",
            },
            {
                "title": "Alice In Borderland",
                "description": "Obsessed gamer Arisu suddenly finds himself in a strange, emptied-out version of Tokyo in which he and his friends must compete in dangerous games in order to survive.",
                "img": "ali.jpg",
                "genre": "Thriller",
                "trailer_url": "https://www.youtube.com/embed/49_44FFKZ1M",
            },

        ]

        for series_data in series_data:
            existing_series = Series.query.filter_by(title=series_data["title"]).first()
            if not existing_series:
                new_series = Series(**series_data)
                new_series.create()