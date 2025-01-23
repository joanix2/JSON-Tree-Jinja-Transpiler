from flask import Flask, request, jsonify
import os
from src.parser import parse_xml_file
from src.build import build_infrastructure
import hashlib
import xml.etree.ElementTree as ET
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

app = Flask(__name__)

# Configuration de la clé secrète pour JWT
app.config["JWT_SECRET_KEY"] = "votre_cle_secrete_pour_jwt"  # Changez cette clé pour quelque chose de sécurisé
jwt = JWTManager(app)

# Chemin par défaut pour l'infrastructure
BASE_OUTPUT_DIR = os.path.join("output")
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

# Utilisateurs fictifs pour l'authentification
USERS = {
    "admin": "password123",
    "user": "userpassword"
}

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint pour s'authentifier et obtenir un token JWT.
    """
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")

    # Vérification des identifiants
    if username in USERS and USERS[username] == password:
        # Crée un token JWT pour l'utilisateur
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect"}), 401

@app.route('/compile', methods=['POST'])
@jwt_required()
def compile_endpoint():
    """
    Endpoint pour traiter un fichier XML envoyé directement 
    dans le body de la requête (content-type : text/xml ou application/xml).
    """
    try:

        # Récupérer l'utilisateur connecté (du JWT)
        current_user = get_jwt_identity()
        print(f"Requête effectuée par : {current_user}")

        # 1. Récupère le contenu brut de la requête
        xml_content = request.get_data(as_text=True)  # as_text=True => str, sinon bytes
        
        # 2. Créer un hash du contenu XML
        hash_value = hashlib.md5(xml_content.encode('utf-8')).hexdigest()
        
        # 3. Créer un dossier nommé avec ce hash
        output_dir = os.path.join(BASE_OUTPUT_DIR, hash_value)
        os.makedirs(output_dir, exist_ok=True)
        
        # 4. Parser l’arbre XML en mémoire (sans passer par un fichier)
        try:
            root = ET.fromstring(xml_content)
            infrastructure_path = os.path.join(output_dir, "infrastructure.yml")
            # Appelle la fonction pour traiter le fichier XML
            parse_xml_file(root, infrastructure_path)
        except ET.ParseError as e:
            return jsonify({"error": f"Erreur de parsing XML: {e}"}), 400
        
        return jsonify({
            "message": "Fichiers générés avec succès.",
            "id": hash_value,
            "output_dir": output_dir
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/build', methods=['POST'])
@jwt_required()
def build_endpoint():
    """
    Endpoint pour générer une arborescence de projet à partir d'un fichier YAML.

    Paramètres (JSON dans le body de la requête) :
        - config_file (str) : chemin vers le fichier YAML décrivant la structure du projet 
                             (par défaut : output/infrastructure.yml)
    """

    data = request.get_json(force=True)
    id = data.get('id')
    config_file = os.path.join(BASE_OUTPUT_DIR, id, "infrastructure.yml")

    try:
        # Appelle la fonction pour construire l'infrastructure
        build_infrastructure(config_file)
        return jsonify({
            "message": "Arborescence générée avec succès.",
            "config_file": config_file
        }), 200
    except FileNotFoundError:
        return jsonify({
            "error": f"Fichier introuvable : {config_file}"
        }), 404
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Par défaut, Flask écoute sur le port 5000
    app.run(debug=True)
