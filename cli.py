import click
from src.parser import parse_xml_file

@click.command()
@click.argument("input_file", type=click.Path(exists=True), default="main.xml")
@click.option("--output-dir", "-o", type=click.Path(), default="output", help="Répertoire de sortie pour les fichiers générés.")
def cli(input_file, output_dir):
    """
    CLI pour traiter un fichier XML et générer des fichiers à partir de templates.

    Arguments :
        INPUT_FILE : Le fichier XML à traiter (par défaut : main.xml).

    Options :
        --output-dir, -o : Répertoire de sortie pour les fichiers générés (par défaut : 'output').
    """
    click.echo(f"Processing XML file: {input_file}")
    click.echo(f"Output directory: {output_dir}")

    try:
        # Appelle la fonction pour traiter le fichier XML
        parse_xml_file(input_file, output_dir)
        click.echo("Processing completed successfully.")
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)

if __name__ == "__main__":
    cli()
