import json
import os
import xml.etree.ElementTree as ET

from .src.build import build_infrastructure
from .src.converter import xml_to_dict
from .src.parser import parse_json_file
from .src.validator import check_tree

def convert_xml_to_json(xml_file, json_file):
    """
    Convertit un fichier XML en JSON.

    Options :
        xml_file : Fichier XML source.
        --json-file, -j : Fichier JSON de sortie (facultatif).
                         Par défaut, le JSON aura le même nom et se trouvera dans le même répertoire que le fichier XML.
    """
    # Déterminer le fichier JSON de sortie par défaut s'il n'est pas fourni
    if json_file is None:
        json_file = os.path.splitext(xml_file)[0] + ".json"

    tree = ET.parse(xml_file)
    root = tree.getroot()

    json_data = xml_to_dict(root)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

def compile_json(templates_path, input_file, type, output):
    """
    Traite un fichier JSON et génère des fichiers à partir de templates.

    Arguments :
        INPUT_FILE : Le fichier JSON à traiter (par défaut : main.json).

    Options :
        --type, -t : Choix du type de compilation du premier nœud (par défaut : 'default').
        --output-dir, -o : Répertoire de sortie pour les fichiers générés (par défaut : 'output').
    """

    # Charger et parser le fichier JSON
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        
    if not check_tree(json_data):
        raise ValueError("❌ Erreur : Le fichier JSON n'est pas un arbre valide.")

    # Appelle la fonction pour traiter le fichier JSON
    parse_json_file(templates_path, json_data, type, output)

def transpile_xml_or_json(templates_path, input_file, type, output):
    """
    Exécute toutes les étapes :
    1. Vérifie si le fichier est XML ou JSON.
    2. Convertit le fichier XML en JSON si nécessaire.
    3. Parse le JSON.
    4. Si le parsing réussit, génère une arborescence YAML.

    Arguments :
        INPUT_FILE : Le fichier XML ou JSON à traiter.

    Options :
        --type, -t : Choix du type de compilation du premier nœud.
        --output, -o : Répertoire de sortie pour les fichiers générés.
    """
    
    file_ext = os.path.splitext(input_file)[1].lower()

    if file_ext not in [".xml", ".json"]:
        raise ValueError("❌ Erreur : Le fichier d'entrée doit être au format XML ou JSON.")

    json_file = input_file  # Par défaut, c'est le JSON s'il est déjà en JSON

    if file_ext == ".xml":
        # Convertir XML en JSON
        json_file = os.path.splitext(input_file)[0] + ".json"
        
        tree = ET.parse(input_file)
        root = tree.getroot()
        json_data = xml_to_dict(root)

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

    # Charger et parser le fichier JSON
    compile_json(templates_path, json_file, type, output)

    # Génération de l'arborescence à partir du YAML
    build_infrastructure(output)