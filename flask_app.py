from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import redirect
from flask import url_for
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from wtforms.validators import ValidationError

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

db = SQLAlchemy(app)

Bootstrap(app)

nav = Nav(app)

SSLify(app)

@nav.navigation('mysite_navbar')
def create_navbar():
    home_view = View('Home', 'homepage')
    register_view = View('Register', 'register')
    about_me_view = View('About Me', 'about_me')
    class_schedule_view = View('Class Schedule', 'class_schedule')
    top_ten_songs_view = View('Top Ten Songs', 'top_ten_songs')
    misc_subgroup = Subgroup('Misc',
                             about_me_view,
                             class_schedule_view,
                             top_ten_songs_view)
    return Navbar('MySite', home_view, misc_subgroup, register_view)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer)
    name = db.Column(db.String(80))
    teacher_name = db.Column(db.String(80))
    resource_name = db.Column(db.String(80))
    resource_url = db.Column(db.String(300))

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField(
        'Email', validators=[InputRequired(), Email()])
    password = PasswordField(
        'Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please choose a different username.')


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    artist_name = db.Column(db.String(80))
    youtube_url = db.Column(db.String(300))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    email = db.Column(db.String(150))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/aboutme')
@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/class_schedule')
def class_schedule():
    courses = Course.query.all()
    return render_template('class_schedule.html',
                           courses=courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('register.html', form=form)

@app.route('/top_ten_songs')
def top_ten_songs():
    songs = Song.query.all()
    return render_template('top_ten_songs.html',
                            songs=songs)

if __name__ == '__main__':
  db.create_all()



