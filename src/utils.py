import json

def load_file(file_path):
    """Charge le contenu d'un fichier JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {file_path}")
    except json.JSONDecodeError:
        print(f"❌ Erreur de décodage JSON dans le fichier: {file_path}")
