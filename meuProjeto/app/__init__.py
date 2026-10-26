from app.database import init_db
from config import Config
from flask import Flask

def Create_app():
  # Adicionamos static_folder='../static' para o Flask achar o CSS
  app = Flask(
      __name__, template_folder='views'
  )  # Ajuste o caminho se necessário conforme a raiz
  app.config.from_object(Config)

  # Inicia o banco de dados
  init_db()

  from .controllers.meu_cine import mf_bp

  app.register_blueprint(mf_bp)

  return app