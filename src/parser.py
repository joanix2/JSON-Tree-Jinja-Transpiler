import os
import xml.etree.ElementTree as ET
from src.node import Node
from src.jinja.template_services import get_template

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
    children = []
    for child in xml_node:
        child_node = rec_xml_parser(child)
        children.append(child_node)

    template_name = f"{xml_node.tag}.jinja"
    template = get_template(template_name)

    return Node(tag=xml_node.tag, template=template, children=children, **xml_node.attrib)

def parse_xml_file(xml_file_path, output_file=OUTPUT_XML_FILE):
    """
    Parse an XML file and consolidate all rendered content into a single XML file.

    :param xml_file_path: Path to the XML file to parse.
    :param output_file: Path to the consolidated output XML file.
    """
    # Load and parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Start the recursive parsing process
    root_node = rec_xml_parser(root)
    print(root_node)

    # Render the entire tree starting from the root node
    rendered_content = root_node.compile()

    # Write the rendered content to the output file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_content)

    print(f"Consolidated XML file generated at: {output_file}")
