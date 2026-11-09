from app.model.movie import Movie
from app.model.user import User
from app.model.review import Review
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

mf_bp = Blueprint('filme', __name__)

# --- Rota para Adicionar um Novo Filme no Catálogo ---
@mf_bp.route('/filmes/novo', methods=['GET', 'POST'])
def adicionar_filme():
    if 'user_id' not in session:
        flash('Faz login para cadastrar um filme.', 'error')
        return redirect(url_for('filme.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        release_year = request.form.get('release_year')
        poster_url = request.form.get('poster_url')
        synopsis = request.form.get('synopsis')

        Movie.create(title, release_year, poster_url, synopsis)
        flash('Filme adicionado ao catálogo com sucesso!', 'success')
        return redirect(url_for('filme.listar_filmes'))

    return render_template('adicionar_filme.html')

# --- Rota para Deixar uma Nota e Impressão de um Filme ---
@mf_bp.route('/filmes/<int:movie_id>/avaliar', methods=['GET', 'POST'])
def avaliar_filme(movie_id):
    if 'user_id' not in session:
        flash('Faz login para registrar a tua avaliação.', 'error')
        return redirect(url_for('filme.login'))

    movie = Movie.find_by_id(movie_id)
    if not movie:
        flash('Filme não encontrado.', 'error')
        return redirect(url_for('filme.listar_filmes'))

    if request.method == 'POST':
        rating = float(request.form.get('rating', 5.0))
        is_fresh = 1 if request.form.get('is_fresh') == 'on' else 0
        content = request.form.get('content')

        Review.create(
            user_id=session['user_id'],
            movie_id=movie_id,
            rating=rating,
            is_fresh=is_fresh,
            content=content
        )
        flash(f'Adicionaste "{movie.title}" à tua estante!', 'success')
        return redirect(url_for('filme.estante'))

    return render_template('avaliar_filme.html', movie=movie)

# --- Rota da Estante Pessoal (Estilo Letterboxd) ---
@mf_bp.route('/estante')
def estante():
    if 'user_id' not in session:
        flash('Faz login para veres a tua estante.', 'error')
        return redirect(url_for('filme.login'))

    reviews = Review.find_by_user(session['user_id'])
    return render_template('estante.html', reviews=reviews)
@mf_bp.route('/')
def index():
  return render_template('home.html')


@mf_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.find_by_email(email)
    if user and user.check_password(password):
      session['user_id'] = user.id
      session['username'] = user.username
      flash(f'Bem-vindo(a) de volta, {user.username}!', 'success')
      return redirect(url_for('filme.home'))
    else:
      flash('Tente novamente! Informações inválidas.', 'error')

  return render_template('login.html')


@mf_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = User.create(username, email, password)
    if new_user:
      flash('Cadastro realizado com sucesso! Faça login para continuar.')
      return redirect(url_for('filme.login'))

    flash('Erro ao cadastrar. E-mail ou Nome de Usuário já em uso.', 'error')

  return render_template('cadastro.html')


@mf_bp.route('/logout')
def logout():
  session.clear()
  flash('Você saiu da sua sessão.', 'success')
  return redirect(url_for('filme.login'))


@mf_bp.route('/home')
def home():
  movies = Movie.get_all()
  return render_template('home.html', movies=movies)


@mf_bp.route('/filmes')
def listar_filmes():
  if 'user_id' not in session:
    flash('Por favor, faça login para aceder à lista de filmes.', 'error')
    return redirect(url_for('filme.login'))
  movies = Movie.get_all()
  return render_template('lista_filmes.html', movies=movies)