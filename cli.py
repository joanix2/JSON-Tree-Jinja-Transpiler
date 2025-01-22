import os
import click
from src.parser import parse_xml_file
from src.build import build_infrastructure
import xml.etree.ElementTree as ET
from src.tests_gen.xml_tree import process_xml_file

INFRASTRUCTURE = os.path.join("output","infrastructure.yml")
TEST_OUTPUT_DIR = os.path.join("output", "tests")

# Ensure the output directory exists
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

@click.group()
def cli():
    """
    CLI pour la gestion des templates et des projets.
    """
    pass

@cli.command()
@click.argument("input_file", type=click.Path(exists=True), default="main.xml")
@click.option("--output-dir", "-o", type=click.Path(), default=INFRASTRUCTURE, help="Répertoire de sortie pour les fichiers générés.")
def compile(input_file, output_dir):
    """
    Traite un fichier XML et génère des fichiers à partir de templates.

    Arguments :
        INPUT_FILE : Le fichier XML à traiter (par défaut : main.xml).

    Options :
        --output-dir, -o : Répertoire de sortie pour les fichiers générés (par défaut : 'output').
    """
    click.echo(f"Processing XML file: {input_file}")
    click.echo(f"Output directory: {output_dir}")

    # Load and parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Appelle la fonction pour traiter le fichier XML
    parse_xml_file(root, output_dir)

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
@click.option("--output-dir", "-o", type=click.Path(), default=TEST_OUTPUT_DIR, help="Répertoire de sortie pour les tests générés.")
def generate_tests(input_file, output_dir):
    """
    Génère automatiquement des tests à partir d'un fichier XML.

    Arguments :
        INPUT_FILE : Le fichier XML à traiter (par défaut : main.xml).

    Options :
        --output-dir, -o : Répertoire de sortie pour les fichiers générés (par défaut : 'output/tests').
    """
    click.echo(f"Generating tests from XML file: {input_file}")
    click.echo(f"Tests will be saved in: {output_dir}")

    # Appelle la fonction pour traiter le fichier XML et générer des fichiers de test
    process_xml_file(input_file, output_dir)
    click.echo("Test generation completed.")

if __name__ == "__main__":
    cli()
