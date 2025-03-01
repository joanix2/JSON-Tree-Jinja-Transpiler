import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Template

# Directory for templates
BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
MACROS_DIR = os.path.join(BASE_DIR, "macros")

# Ensure the templates directory exists
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(MACROS_DIR, exist_ok=True)

# Création de l'environnement Jinja2
env = Environment(
    loader=FileSystemLoader([TEMPLATES_DIR, MACROS_DIR]),
    undefined=StrictUndefined  # Lève une erreur si une variable est manquante
)

def get_templates_names(template_folder: str) -> set[str]:
    """
    Retourne un ensemble contenant les noms des fichiers templates (sans l'extension .jinja).
    """
    folder_path = os.path.join(TEMPLATES_DIR, template_folder)

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Le dossier '{folder_path}' n'existe pas.")

    templates_names = set()

    for filename in os.listdir(folder_path):
        if filename.endswith('.jinja'):
            templates_names.add(filename.rsplit('.', 1)[0])  # Retirer l'extension

    return templates_names

def get_template(template_folder: str, template_name: str, params: dict) -> str:
    """
    Charge et rend un template avec les paramètres fournis.
    """
    try:
        template = env.get_template(f"{template_folder}/{template_name}.jinja")
        return template.render(**params)
    except Exception as e:
        raise RuntimeError(f"Erreur lors du rendu du template '{template_folder}/{template_name}.jinja' : {e}")

# def create_template(file_name: str, content: str = ""):
#     """
#     Create a new template file with the given name and optional content.
    
#     :param file_name: Name of the template file to create.
#     :param content: Initial content to write into the template (default is empty).
#     """
#     file_path = os.path.join(TEMPLATE_DIR, file_name)
#     if os.path.exists(file_path):
#         raise FileExistsError(f"Template file '{file_name}' already exists.")
    
#     with open(file_path, 'w') as template_file:
#         template_file.write(content)
#     print(f"Template '{file_name}' created successfully.")

# def update_template(file_name: str, new_content: str):
#     """
#     Update an existing template file with new content.
    
#     :param file_name: Name of the template file to update.
#     :param new_content: New content to replace the existing template content.
#     """
#     file_path = os.path.join(TEMPLATE_DIR, file_name)
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Template file '{file_name}' does not exist.")
    
#     with open(file_path, 'w') as template_file:
#         template_file.write(new_content)
#     print(f"Template '{file_name}' updated successfully.")
