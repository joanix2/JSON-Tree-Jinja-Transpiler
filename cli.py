import json
import os
import click
from src.converter import xml_to_dict
from src.parser import parse_json_file
from src.build import build_infrastructure
from src.watcher import start_watching
import xml.etree.ElementTree as ET

INFRASTRUCTURE = os.path.join("output","infrastructure.yml")

@click.group()
def cli():
    """
    CLI pour la gestion des templates et des projets.
    """
    pass

@cli.command()
@click.argument("xml_file", type=click.Path(exists=True), required=True)
@click.option("--json-file", "-j", type=click.Path(), default=None, help="Fichier JSON de sortie. Par défaut, même nom que le fichier XML avec extension .json.")
def convert(xml_file, json_file):
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

    click.echo(f"Conversion de {xml_file} en {json_file}...")

    tree = ET.parse(xml_file)
    root = tree.getroot()

    json_data = xml_to_dict(root)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    click.echo(f"Conversion terminée. Résultat enregistré dans {json_file}")

@cli.command()
@click.argument("input_file", type=click.Path(exists=True), default="main.json")
@click.option("--type", "-t", type=str, default="default", help="Choix du type de compilation du premier nœud.")
@click.option("--output", "-o", type=click.Path(), default=INFRASTRUCTURE, help="Répertoire de sortie pour les fichiers générés.")
def compile(input_file, type, output):
    """
    Traite un fichier JSON et génère des fichiers à partir de templates.

    Arguments :
        INPUT_FILE : Le fichier JSON à traiter (par défaut : main.json).

    Options :
        --type, -t : Choix du type de compilation du premier nœud (par défaut : 'default').
        --output-dir, -o : Répertoire de sortie pour les fichiers générés (par défaut : 'output').
    """
    click.echo(f"Processing JSON file: {input_file}")
    click.echo(f"Output file: {output}")

    # Charger et parser le fichier JSON
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Appelle la fonction pour traiter le fichier JSON
    parse_json_file(json_data, type, output)

@cli.command()
@click.option("--config-file", "-c", type=click.Path(exists=True), default=INFRASTRUCTURE, help="Fichier YAML décrivant l'arborescence.")
def build(config_file):
    """
    Génère une arborescence de projet à partir d'un fichier YAML.

    Options :
        --config-file, -c : Fichier YAML décrivant la structure du projet (par défaut : 'infrastructure.yml').
    """
    click.echo(f"Loading configuration from: {config_file}")
    build_infrastructure(config_file)

@cli.command()
@click.argument("input_file", type=click.Path(exists=True), default="main.xml")
@click.option("--type", "-t", type=str, default="default", help="Choix du type de compilation du premier nœud.")
@click.option("--output", "-o", type=click.Path(), default=INFRASTRUCTURE, help="Répertoire de sortie pour les fichiers générés.")
def run(input_file, type, output):
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
        click.echo("❌ Erreur : Le fichier d'entrée doit être au format XML ou JSON.", err=True)
        return

    json_file = input_file  # Par défaut, c'est le JSON s'il est déjà en JSON

    if file_ext == ".xml":
        # Convertir XML en JSON
        json_file = os.path.splitext(input_file)[0] + ".json"
        click.echo(f"🔄 Conversion de {input_file} en JSON...")
        
        tree = ET.parse(input_file)
        root = tree.getroot()
        json_data = xml_to_dict(root)

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        click.echo(f"✅ Conversion terminée : {json_file}")

    # Charger et parser le fichier JSON
    click.echo(f"🔍 Parsing du fichier JSON : {json_file}")
    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    parse_json_file(json_data, type, output)

    # Génération de l'arborescence à partir du YAML
    click.echo(f"🛠️ Génération de l'arborescence depuis {output}")
    build_infrastructure(output)

    click.echo("✅ Exécution complète ! 🚀")

@cli.command()
@click.argument("target_file", type=click.Path(exists=True), default="main.xml")
def start(target_file):
    """
    Démarre l'observateur qui surveille les fichiers et recompile automatiquement.

    Arguments :
        target_file : Le fichier XML ou JSON à traiter.
    """
    click.echo(f"👀 Surveillance activée sur : {target_file} et le dossier templates/\n")
    start_watching(target_file)

if __name__ == "__main__":
    cli()
