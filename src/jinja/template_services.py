import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Template

# Directory for templates
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

# Ensure the templates directory exists
os.makedirs(TEMPLATE_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def create_template(file_name: str, content: str = ""):
    """
    Create a new template file with the given name and optional content.
    
    :param file_name: Name of the template file to create.
    :param content: Initial content to write into the template (default is empty).
    """
    file_path = os.path.join(TEMPLATE_DIR, file_name)
    if os.path.exists(file_path):
        raise FileExistsError(f"Template file '{file_name}' already exists.")
    
    with open(file_path, 'w') as template_file:
        template_file.write(content)
    print(f"Template '{file_name}' created successfully.")

def update_template(file_name: str, new_content: str):
    """
    Update an existing template file with new content.
    
    :param file_name: Name of the template file to update.
    :param new_content: New content to replace the existing template content.
    """
    file_path = os.path.join(TEMPLATE_DIR, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Template file '{file_name}' does not exist.")
    
    with open(file_path, 'w') as template_file:
        template_file.write(new_content)
    print(f"Template '{file_name}' updated successfully.")

def compile_template(template_name: str, args: dict) -> str:
    """
    Compile a template by filling it with the provided arguments.
    
    :param template_name: Name of the template file to compile.
    :param args: Dictionary of arguments to render in the template.
    :return: Rendered template content as a string.
    """   
    template = get_template(template_name)
    rendered_content = template.render(args)
    return rendered_content

def get_template(template_name: str) -> Template:
    file_path = os.path.join(TEMPLATE_DIR, template_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Template file '{template_name}' does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    
    return Template(template_content, undefined=StrictUndefined)
