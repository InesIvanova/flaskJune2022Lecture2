from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@' \
                                        f'localhost:{config("DB_PASSWORD")}/{config("DB_NAME")}'
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


class BookModel(db.Model):
    __tablename__ = 'books'

    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    reader_pk = db.Column(db.Integer, db.ForeignKey("readers.pk"))
    reader = db.relationship("ReaderModel")

    def __repr__(self):
        return f"<{self.pk}> {self.title} from {self.author}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReaderModel(db.Model):
    __tablename__ = "readers"

    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    books = db.relationship("BookModel", backref="book", lazy='dynamic')


class Books(Resource):
    def get(self):
        books = BookModel.query.all()
        books_data = [b.as_dict() for b in books]
        return {"books": books_data}

    def post(self):
        data = request.get_json()
        book = BookModel(**data)
        db.session.add(book)
        db.session.commit()
        return book.as_dict()


api.add_resource(Books, "/books/")


if __name__ == '__main__':
    app.run(debug=True)