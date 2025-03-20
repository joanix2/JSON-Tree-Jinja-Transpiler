import os

from .templates_manager import TemplateManager
from .node import Node

# Fichier de sortie par défaut
INFRASTRUCTURE = os.path.join("output","infrastructure.yml")

# S'assurer que le répertoire de sortie existe
os.makedirs(os.path.dirname(INFRASTRUCTURE), exist_ok=True)

def rec_json_parser(templates_manager: TemplateManager,json_node):
    """
    Analyse récursivement un nœud JSON et ses enfants, retournant un objet Node
    qui se rend lui-même et ses enfants.

    :param json_node: Le nœud JSON actuel sous forme de dictionnaire.
    :return: Un objet Node représentant l'élément JSON et ses enfants.
    """
    # Récupérer le tag du nœud
    tag = json_node.get("tag", "unknown")

    # Récupérer les enfants s'ils existent
    children = [rec_json_parser(templates_manager, child) for child in json_node.get("children", [])]

    # Récupérer le contenu textuel s'il existe
    value = json_node.get("value")

    # Récupérer les attributs (tous sauf "tag", "children" et "value")
    attributes = json_node.get("attributes", {})

    return Node(templates_manager=templates_manager, tag=tag, children=children, value=value, **attributes)

def parse_json_file(templates_path: str, json_tree_root, type, output_file=INFRASTRUCTURE):
    """
    Parse un fichier JSON et consolide tout le contenu rendu dans un seul fichier JSON.

    :param json_tree_root: Dictionnaire JSON représentant la racine du fichier JSON.
    :param type: Type de compilation du nœud root.
    :param output_file: Fichier de sortie YAML.
    """
    templates_manager = TemplateManager(templates_path)

    # Démarrer le processus de parsing récursif
    root_node = rec_json_parser(templates_manager, json_tree_root)

    # Rendre l'arbre entier à partir du nœud racine
    rendered_content = getattr(root_node, type)

    # Write the rendered content to the output file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_content)

    print(f"File generated at: {output_file}")
