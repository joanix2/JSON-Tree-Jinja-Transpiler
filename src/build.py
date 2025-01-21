import os
import xml.etree.ElementTree as ET

def create_structure(base_path, structure):
    """
    Crée une arborescence de répertoires et fichiers à partir de la structure donnée.
    
    :param base_path: Répertoire de base pour créer l'arborescence.
    :param structure: Liste des éléments XML décrivant les répertoires et fichiers.
    """
    for item in structure:
        if item.tag == "directory":
            # Récupérer le nom du répertoire
            dir_name = item.get("name")
            dir_path = os.path.join(base_path, dir_name)

            # Créer le répertoire
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")

            # Créer les enfants récursivement si présents
            children = list(item)
            if children:
                create_structure(dir_path, children)

        elif item.tag == "file":
            # Récupérer le nom du fichier
            file_name = item.get("name")
            file_path = os.path.join(base_path, file_name)

            # Récupérer le contenu
            content = item.find("content").text if item.find("content") is not None else ""

            # Créer le fichier avec le contenu donné
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Created file: {file_path}")

def build_infrastructure(config_file):
    """
    Génère une arborescence de fichiers et répertoires à partir d'un fichier XML.
    
    :param config_file: Chemin du fichier XML de configuration.
    """
    try:
        # Charger le fichier XML
        tree = ET.parse(config_file)
        root = tree.getroot()

        # Récupérer les informations principales
        project_name = root.find("project_name").text
        output_dir = root.find("output_dir").text
        structure = root.find("structure")

        # Chemin de base
        base_path = os.path.join(output_dir, project_name)

        # Créer la structure de l'arborescence
        os.makedirs(base_path, exist_ok=True)
        create_structure(base_path, structure)

        print(f"Project structure generated in: {base_path}")

    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found.")
    except ET.ParseError as e:
        print(f"Error parsing XML file '{config_file}': {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
