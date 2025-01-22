import os
import xml.etree.ElementTree as ET
from jinja2 import Template
import hashlib

# Directory for output files
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_and_generate(xml_element: ET.Element, output_dir: str = OUTPUT_DIR):
    """
    Recursive function to parse an XML element and generate a file for each subtree.
    
    :param xml_element: The current XML element to process.
    :param output_dir: Directory where the generated files will be saved.
    """
    # Extract content for the current element
    content = f"<{xml_element.tag}"
    # Add attributes if present
    if xml_element.attrib:
        content += " " + " ".join([f'{key}="{value}"' for key, value in xml_element.attrib.items()])
    content += ">\n"

    # Add child content
    for child in xml_element:
        child_content = ET.tostring(child, encoding='unicode')
        content += f"  {child_content}\n"

    content += f"</{xml_element.tag}>\n"

    # Generate a unique file name using a hash of the content
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    file_name = f"{xml_element.tag}_{content_hash}.xml"
    file_path = os.path.join(output_dir, file_name)
    
    # Write the current element's content to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Generated file: {file_path}")

    # Recursively process child elements
    for child in xml_element:
        child_output_dir = os.path.join(output_dir, child.tag)
        os.makedirs(child_output_dir, exist_ok=True)  # Create a subdirectory for each child tag
        parse_and_generate(child, child_output_dir)

def process_xml_file(xml_file_path: str, output_dir: str = OUTPUT_DIR):
    """
    Parse an XML file and generate a file for each subtree.

    :param xml_file_path: Path to the XML file to process.
    :param output_dir: Directory where the generated files will be saved.
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Start processing from the root element
        parse_and_generate(root, output_dir)
        print(f"XML processing completed. Files are saved in '{output_dir}'.")

    except ET.ParseError as e:
        print(f"Error parsing XML file '{xml_file_path}': {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
