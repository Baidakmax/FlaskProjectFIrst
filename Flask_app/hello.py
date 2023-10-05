from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask import render_template
from flask_admin.contrib.sqla import ModelView
from flask_marshmallow import Marshmallow
from flask_restx import Resource, Api
# from models import User, Footballer, db
from flask_migrate import Migrate


ma = Marshmallow()


app = Flask(__name__)
api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_db.db"
app.config['FLASK_ADMIN_SWATCH'] = 'united'
app.config['SECRET_KEY'] = 'the random string'

db = SQLAlchemy()
migrate = Migrate(app, db, command='migrate')



admin = Admin(app, name='flask app admin', template_mode='bootstrap4')
db.init_app(app)
ma.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.String(10))
    email = db.Column(db.String)

class Footballer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String, unique=True, nullable=False)
    surname = db.Column(db.String)
    age = db.Column(db.String(10))
    number_player = db.Column(db.Float)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class FootballerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Footballer


@app.route("/")
def hello_world():
    return render_template('hello.html')


@api.route('/user_list/', endpoint="user_list")
class UserList(Resource):
    def get(self):
        list_schema = UserSchema(many=True)
        return list_schema.dump(User.query.all()), 200

@api.route('/football_list/', endpoint="football_list")
class FootballerList(Resource):
    def get(self):
        list_schema = FootballerSchema(many=True)
        return list_schema.dump(Footballer.query.all()), 200

with app.app_context():
    db.create_all()


# Flask and Flask-SQLAlchemy initialization here
admin.add_view(ModelView(Footballer, db.session))
admin.add_view(ModelView(User, db.session))


if __name__ == "__main__":
    app.run(debug=True)
