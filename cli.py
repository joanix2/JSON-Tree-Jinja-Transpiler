import os
import click
from src.parser import parse_xml_file
from src.build import build_infrastructure

INFRASTRUCTURE = os.path.join("output","infrastructure.yml")

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

    # Appelle la fonction pour traiter le fichier XML
    parse_xml_file(input_file, output_dir)

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


if __name__ == "__main__":
    cli()
