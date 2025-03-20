import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Template
from typing import Dict, Set

class TemplateManager:
    """
    Gestionnaire des templates Jinja.
    """

    def __init__(self, base_dir: str = None):
        """
        Initialise l'environnement Jinja et vérifie l'existence des répertoires.
        """
        self.base_dir = base_dir if base_dir else os.path.dirname(__file__)
        self.templates_dir = os.path.join(self.base_dir, "templates")
        self.macros_dir = os.path.join(self.base_dir, "macros")

        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.macros_dir, exist_ok=True)

        self.env = Environment(
            loader=FileSystemLoader([self.templates_dir, self.macros_dir]),
            undefined=StrictUndefined  # Lève une erreur si une variable est manquante
        )

    def get_templates_names(self, template_folder: str) -> Set[str]:
        """
        Retourne un ensemble contenant les noms des fichiers templates (sans l'extension .jinja).

        :param template_folder: Le dossier contenant les templates.
        :return: Un ensemble des noms des templates disponibles.
        """
        folder_path = os.path.join(self.templates_dir, template_folder)

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Le dossier '{folder_path}' n'existe pas.")

        templates_names = {
            filename.rsplit('.', 1)[0]
            for filename in os.listdir(folder_path) if filename.endswith('.jinja')
        }

        return templates_names

    def get_template(self, template_folder: str, template_name: str, params: Dict) -> str:
        """
        Charge et rend un template avec les paramètres fournis.

        :param template_folder: Le dossier contenant le template.
        :param template_name: Le nom du fichier template (sans l'extension).
        :param params: Un dictionnaire de variables pour le rendu.
        :return: Le contenu rendu du template sous forme de chaîne.
        """
        try:
            template_path = f"{template_folder}/{template_name}.jinja"
            template = self.env.get_template(template_path)
            return template.render(**params)
        except Exception as e:
            raise RuntimeError(f"Erreur lors du rendu du template '{template_path}' : {e}")