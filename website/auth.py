from flask import Blueprint

auth = Blueprint('auth',__name__)

@auth.route('/')
def a():
    return "<h1>Auth<h1>"