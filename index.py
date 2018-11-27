from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import programs.random_gen.main as rand_gen
import programs.imc.imc as imc

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
  'db': 'posting-flask',
  'host': 'mongodb://demon:demon123@ds231133.mlab.com:31133/posting-flask'
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = 'PostingSecretKey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Document):
  meta = {'collection': 'users'}
  email = db.StringField(max_length=30)
  password = db.StringField()

@login_manager.user_loader
def load_user(user_id):
  return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
  email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)], render_kw={"placeholder": "Seu e-mail"})
  password = PasswordField('password', validators=[InputRequired(), Length(min=6,max=20)], render_kw={"placeholder": "Sua senha"})

class GenRandForm(FlaskForm):
  lines = IntegerField('lines', validators=[InputRequired()], render_kw={"placeholder":"Insira a quantidade de palavras que deseja"})

class IMCForm(FlaskForm):
  height = FloatField('height', validators=[InputRequired()], render_kw={"placeholder":"Sua altura (ex. 1.82)"})
  weight = FloatField('weight', validators=[InputRequired()], render_kw={"placeholder":"Seu peso (ex. 92.5)"})
  sex = StringField('sex', validators=[InputRequired()], render_kw={"placeholder":"Seu sexo (ex. m/f)"})

class ToDoListForm(FlaskForm):
  title = StringField('title', validators=[InputRequired(), Length(max=30)], render_kw={"placeholder":"Titulo"})
  content = StringField('title', validators=[InputRequired(), Length(min=6)], render_kw={"placeholder":"Texto"})


@app.route('/register', methods=['GET','POST'])
def register():
  if current_user.is_authenticated == True:
    return redirect(url_for('dashboard'))
  form = RegForm()
  if request.method == 'POST':
    if form.validate():
      existing_user = User.objects(email=form.email.data).first()
      if existing_user is None:
        hashpass = generate_password_hash(form.password.data, method='sha256')
        hey = User(form.email.data, hashpass).save()
        login_user(hey)
        return redirect(url_for('index'))
  return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
  if current_user.is_authenticated == True:
    return redirect(url_for('index'))
  form = RegForm()
  if request.method == 'POST':
    if form.validate():
      check_user = User.objects(email=form.email.data).first()
      if check_user:
        if check_password_hash(check_user['password'], form.password.data):
          login_user(check_user)
          return redirect(url_for('index'))
  return render_template('auth/login.html', form=form)

@app.route('/')
@login_required
def index():
  username = current_user.email.split('@')
  return render_template('index.html', name=username[0])
  
@app.route('/gerador-aleatorio', methods=['GET','POST'])
@login_required
def gerador():
  form = GenRandForm()
  if request.method == 'POST':
    if form.validate():
      wordlist = rand_gen.ret_list(None, form.lines.data)
      return render_template('pages/gerador/gerador.html', wordlist=wordlist)

  return render_template('pages/gerador/gerador.html', form=form)

@app.route('/imc', methods=['GET','POST'])
def imcCheck():
  form = IMCForm()
  if request.method == 'POST':
    if form.validate():
      ret_value = imc.calculate(form.sex.data, form.height.data, form.weight.data)
      imc_final = ret_value.split('@')
      return render_template('pages/imc/imc.html', imc_value=imc_final[0], imc_result=imc_final[1])

  return render_template('pages/imc/imc.html', form=form)

@app.route('/imc', methods=['GET','POST'])
def todoList():
  form = ToDoListForm()

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))