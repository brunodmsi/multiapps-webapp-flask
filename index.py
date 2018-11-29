from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import programs.random_gen.main as rand_gen
import programs.imc.imc as imc
from programs.vigenere.vigenere import Vigenere
from programs.blockchain.chain import Chain
import programs.pass_generator.gen as pass_gen

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
  'db': 'posting-flask',
  'host': 'mongodb://demon:demona12345@ds029745.mlab.com:29745/multiapps-webapp-flask'
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

class TodoList(db.Document):
  meta = {'collection': 'todolists'}
  user_id = db.ReferenceField(User)
  title = db.StringField(max_length=30)
  content = db.StringField()

class Person(db.Document):
  meta = {'collection': 'persons'}
  registeredBy = db.ReferenceField(User)
  staffcode = db.StringField(max_length=10)
  firstname = db.StringField(max_length=30)
  lastname = db.StringField(max_length=30)

@login_manager.user_loader
def load_user(user_id):
  return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
  email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)], render_kw={"placeholder": "Seu e-mail"})
  password = PasswordField('password', validators=[InputRequired(), Length(min=6,max=20)], render_kw={"placeholder": "Sua senha"})

class PersonForm(FlaskForm):
  staffnum = StringField('email', validators=[InputRequired(), Length(max=10)], render_kw={"placeholder": "Codigo Staff"})
  firstname = StringField('email', validators=[InputRequired(), Length(max=30)], render_kw={"placeholder": "Primeiro nome"})
  lastname = StringField('email', validators=[InputRequired(), Length(max=30)], render_kw={"placeholder": "Ultimo nome"})

class GenRandForm(FlaskForm):
  lines = IntegerField('lines', validators=[InputRequired()], render_kw={"placeholder":"Insira a quantidade de palavras que deseja"})

class IMCForm(FlaskForm):
  height = FloatField('height', validators=[InputRequired()], render_kw={"placeholder":"Sua altura (ex. 1.82)"})
  weight = FloatField('weight', validators=[InputRequired()], render_kw={"placeholder":"Seu peso (ex. 92.5)"})
  sex = StringField('sex', validators=[InputRequired()], render_kw={"placeholder":"Seu sexo (ex. m/f)"})

class ToDoListForm(FlaskForm):
  title = StringField('title', validators=[InputRequired(), Length(max=30)], render_kw={"placeholder":"Titulo"})
  content = TextAreaField('title', validators=[InputRequired(), Length(min=5)], render_kw={"placeholder":"Texto"})

class VigenereForm(FlaskForm):
  plaintext = StringField('plaintext', validators=[InputRequired()], render_kw={"placeholder":"Texto para decifrar/codificar"})
  password = StringField('password', validators=[InputRequired()], render_kw={"placeholder":"Senha"})
  decrypt = SelectField(u'Descriptografar', choices=[('false', 'Não'), ('true', 'Sim')])

class BlockchainForm(FlaskForm):
  blocks = IntegerField('blocks', validators=[InputRequired()], render_kw={"placeholder": "Número de blocos a serem criados"})

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

@app.route('/gerador-senha', methods=['GET','POST'])
@login_required
def geradorSenha():
  password = pass_gen.generate()
  return render_template('pages/gerador/gerador-senha.html', password=password)

@app.route('/gerador-aleatorio', methods=['GET','POST'])
@login_required
def gerador():
  form = GenRandForm()
  if request.method == 'POST':
    if form.validate():
      wordlist = rand_gen.ret_list(None, form.lines.data)
      return render_template('pages/gerador/gerador-palavras.html', wordlist=wordlist)
  return render_template('pages/gerador/gerador-palavras.html', form=form)

@app.route('/imc', methods=['GET','POST'])
@login_required
def imcCheck():
  form = IMCForm()
  if request.method == 'POST':
    if form.validate():
      ret_value = imc.calculate(form.sex.data, form.height.data, form.weight.data)
      imc_final = ret_value.split('@')
      return render_template('pages/imc/imc.html', imc_value=imc_final[0], imc_result=imc_final[1])

  return render_template('pages/imc/imc.html', form=form)

@app.route('/blockchain', methods=['GET','POST'])
@login_required
def blockchain():
  form = BlockchainForm()
  if request.method == 'POST':
    if form.validate():
      chain = Chain().generate_chain(form.blocks.data)
      return render_template('pages/blockchain/index.html', chain=chain)
  return render_template('pages/blockchain/index.html', form=form)

@app.route('/vigenere', methods=['GET','POST'])
@login_required
def vigenere():
  form = VigenereForm()
  if request.method == 'POST':
    if form.validate():
      decrypt = form.decrypt.data
      if decrypt == 'false': decrypt = False
      if decrypt == 'true': decrypt = True
      vig = Vigenere().encrypt(form.plaintext.data, form.password.data, decrypt)
      return render_template('pages/vigenere/vigenere.html', vig=vig, decrypt=decrypt, plaintext=form.plaintext.data)

  return render_template('pages/vigenere/vigenere.html', form=form)

@app.route('/todolist', methods=['GET'])
@login_required
def todoListView():
  list = TodoList.objects(user_id=current_user.id)
  return render_template('pages/todolist/index.html', list=list)

@app.route('/todolist/create', methods=['GET','POST'])
@login_required
def todoListCreate():
  form = ToDoListForm()
  if request.method == 'POST':
    if form.validate():
      todo = TodoList(current_user.id, form.title.data, form.content.data).save()
      return redirect('/todolist')
  return render_template('pages/todolist/create.html', form=form)

@app.route('/todolist/<todoId>', methods=['GET'])
@login_required
def todoListShow(todoId):
  todo = TodoList.objects(id=todoId).first()
  if todo.user_id.id != current_user.id:
    return redirect('/')
  return render_template('pages/todolist/show.html', todo=todo)

@app.route('/todolist/delete/<todoId>', methods=['GET'])
@login_required
def todoListDelete(todoId):
  todo = TodoList.objects(id=todoId).first()
  if todo.user_id.id != current_user.id:
    return redirect('/')
  todo.delete()
  return redirect('/todolist')

@app.route('/todolist/edit/<todoId>', methods=['GET','POST'])
@login_required
def todoListEdit(todoId):
  form = ToDoListForm()
  if request.method == 'POST':
    if form.validate():
      new_todo = TodoList(id=todoId).update(title=form.title.data, content=form.content.data)
      return redirect('/todolist')
  todo = TodoList.objects(id=todoId).first()
  if todo.user_id.id != current_user.id:
    return redirect('/')
  form.title.data = todo.title
  form.content.data = todo.content
  return render_template('pages/todolist/edit.html', form=form, todo=todo)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

if __name__ == "__main__":
  app.run()
