from flask import request
import jwt
import app_config as config

def validate_token():
    token = None
    user_information = None

    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']

    if not token:
        return 400
    try:
        user_information = jwt.decode(token, key = config.TOKEN_SECRET, algorithms = ["HS256"])
        print(user_information)
    except:
        return 401
        
    return user_information

"""
Ce fichier gère la validation du token JWT.
Lorsqu'une requête est faite aux endpoints protégés, cette fonction vérifie si un token valide est présent dans les en-têtes.
"""