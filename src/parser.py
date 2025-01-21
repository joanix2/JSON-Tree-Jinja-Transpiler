import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring
from src.jinja.template_services import compile_template

# Default output file
OUTPUT_XML_FILE = os.path.join("output","consolidated_output.xml")

# Ensure the output directory exists
os.makedirs(os.path.dirname(OUTPUT_XML_FILE), exist_ok=True)

def rec_xml_parser(xml_node):
    """
    Retourne le rendu Jinja du noeud courant et de ses enfants, en remontant
    une chaîne de caractères qui finira par constituer l'intégralité du code HTML.
    """
    # 1) Rendre récursivement tous les enfants
    children_renders = []
    for child in xml_node:
        child_render = rec_xml_parser(child)
        children_renders.append(child_render)

    # 2) Concaténation des arguments
    context = {
        **xml_node.attrib,
        "children": children_renders
    }

    # 3) Compiler le template du noeud courant
    template_name = f"{xml_node.tag}.jinja"
    rendered_content = compile_template(template_name, context)

    return rendered_content

def parse_xml_file(xml_file_path, output_file=OUTPUT_XML_FILE):
    """
    Parse an XML file and consolidate all rendered content into a single XML file.

    :param xml_file_path: Path to the XML file to parse.
    :param output_file: Path to the consolidated output XML file.
    """
    try:
        # Load and parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Start the recursive parsing process
        xml_render = rec_xml_parser(root)

        with open(output_file, "w") as f:
            f.write(xml_render)

        print(f"Consolidated XML file generated at: {output_file}")

    except ET.ParseError as e:
        print(f"Error parsing XML file '{xml_file_path}': {e}")
    except Exception as e:
        print(f"Error processing XML file '{xml_file_path}': {e}")
