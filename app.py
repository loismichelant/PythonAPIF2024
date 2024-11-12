from flask import Flask
from views.user_view import user

app = Flask(__name__)

app.register_blueprint(user)

@app.route('/', methods=['GET'])
def home():
    return "<h1>HOME 2</h1>"

# client = MongoClient("mongodb+srv://loism1508:NWJG656RNiD20o7n@cluster0.m7gsv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client['LS3FALL2024']
# users_collection = db['Users']

if __name__ == '__main__':
    app.run()

"""
Ce fichier est le point d’entrée de l’application. Il crée une instance de l'application Flask et définit les routes de base.
La ligne app.register_blueprint(user) permet d'intégrer les routes définies dans user_view.py, qui gère les utilisateurs.
La route '/' est une simple page d’accueil renvoyant du HTML.
La partie commentée contient la connexion à MongoDB via MongoClient, mais elle est déportée dans db.py via la classe Database.
"""