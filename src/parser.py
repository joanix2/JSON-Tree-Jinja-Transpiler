import os
import xml.etree.ElementTree as ET
from src.jinja.template_service import compile_template

# Default output directory
OUTPUT_DIR = "output"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def rec_xml_parser(xml_tree, output_dir=OUTPUT_DIR):
    """
    Recursive function to parse an XML tree and generate files based on templates.

    :param xml_tree: The root of the XML tree to parse.
    :param output_dir: The directory where the generated files will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for child in xml_tree:
        # Get tag name and attributes
        tag = child.tag
        attributes = child.attrib

        # Extract the template name and output file name from the attributes
        template_name = attributes.get("template")
        output_file = attributes.get("output")

        if template_name and output_file:
            # Compile the template with the current attributes
            try:
                rendered_content = compile_template(template_name, attributes)

                # Write the rendered content to the specified output file
                output_path = os.path.join(output_dir, output_file)
                with open(output_path, "w") as output_f:
                    output_f.write(rendered_content)

                print(f"Generated file: {output_path}")

            except Exception as e:
                print(f"Error processing template '{template_name}' for file '{output_file}': {e}")

        # Recursively process child elements
        rec_xml_parser(child, output_dir)

def parse_xml_file(xml_file_path, output_dir=OUTPUT_DIR):
    """
    Parse an XML file and generate files based on the templates specified in the XML.

    :param xml_file_path: Path to the XML file to parse.
    :param output_dir: The directory where the generated files will be saved.
    """
    try:
        # Load and parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Start the recursive parsing process
        rec_xml_parser(root, output_dir)

    except ET.ParseError as e:
        print(f"Error parsing XML file '{xml_file_path}': {e}")
    except Exception as e:
        print(f"Error processing XML file '{xml_file_path}': {e}")
