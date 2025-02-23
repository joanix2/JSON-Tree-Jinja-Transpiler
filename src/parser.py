import os
import xml.etree.ElementTree as ET
from src.node import Node

# Default output file
OUTPUT_XML_FILE = os.path.join("output","consolidated_output.xml")

# Ensure the output directory exists
os.makedirs(os.path.dirname(OUTPUT_XML_FILE), exist_ok=True)

def rec_xml_parser(xml_node):
    """
    Recursively parses an XML node and its children, returning a Node object
    that renders itself and its children.

    :param xml_node: The current XML element.
    :return: A Node object representing the current XML element and its children.
    """
    children = [rec_xml_parser(child) for child in xml_node]

    # Récupérer le contenu textuel s'il existe (en supprimant les espaces inutiles)
    text_content = xml_node.text.strip() if xml_node.text and xml_node.text.strip() else None

    return Node(tag=xml_node.tag, children=children, text=text_content, **xml_node.attrib)


def parse_xml_file(xml_tree_root: ET.Element, output_file=OUTPUT_XML_FILE):
    """
    Parse an XML file and consolidate all rendered content into a single XML file.

    :param xml_file_path: Path to the XML file to parse.
    :param output_file: Path to the consolidated output XML file.
    """

    # Start the recursive parsing process
    root_node = rec_xml_parser(xml_tree_root)

    # Render the entire tree starting from the root node
    rendered_content = root_node.default

    # Write the rendered content to the output file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_content)

    print(f"Consolidated XML file generated at: {output_file}")
