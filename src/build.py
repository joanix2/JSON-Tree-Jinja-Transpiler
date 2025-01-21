import os
import yaml

def create_structure(base_path, structure):
    """
    Crée une arborescence de répertoires et fichiers à partir de la structure donnée.
    
    :param base_path: Répertoire de base pour créer l'arborescence.
    :param structure: Liste des éléments à créer (répertoires ou fichiers).
    """
    for item in structure:
        item_path = os.path.join(base_path, item['name'])

        if item['type'] == 'directory':
            # Créer un répertoire
            os.makedirs(item_path, exist_ok=True)
            print(f"Created directory: {item_path}")

            # Créer les enfants récursivement si présents
            if 'children' in item:
                create_structure(item_path, item['children'])

        elif item['type'] == 'file':
            # Créer un fichier avec le contenu donné
            with open(item_path, 'w') as f:
                f.write(item.get('content', ''))
            print(f"Created file: {item_path}")

def build_infrastructure(config_file):
    try:
        # Charger le fichier YAML
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        # Récupérer les informations principales
        project_name = config['project_name']
        output_dir = config['output_dir']
        structure = config['structure']

        # Chemin de base
        base_path = os.path.join(output_dir, project_name)

        # Créer la structure de l'arborescence
        os.makedirs(base_path, exist_ok=True)
        create_structure(base_path, structure)

        print(f"Project structure generated in: {base_path}")

    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found.", err=True)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{config_file}': {e}", err=True)
    except Exception as e:
        print(f"An error occurred: {e}", err=True)

            