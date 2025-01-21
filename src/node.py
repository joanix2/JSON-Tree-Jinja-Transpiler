from typing import List, Optional
from jinja2 import Template

class Node:
    def __init__(self, tag: str, template:Template, children: Optional[List["Node"]]=None, **args):
        """
        Initialise un nœud avec un tag, un template, des enfants, et des arguments supplémentaires.

        :param tag: Le nom de la balise.
        :param template: Le contenu du template (string).
        :param children: Une liste de nœuds enfants (par défaut, vide).
        :param args: Autres arguments passés pour le rendu du template.
        """
        self.tag = tag
        self.template = template
        self.children = children if children else []
        self.args = args

    def compile(self, output_type=None):
        """
        Compile le template en ajoutant `output_type` aux arguments et en rendant les enfants récursivement.

        :param output_type: Le type de sortie à ajouter aux arguments (ex. 'html' ou 'css').
        :return: Le rendu du template sous forme de chaîne.
        """
        # Vérifie si le nœud a un template
        if not self.template:
            raise ValueError(f"Node '{self.tag}' cannot be compiled because it has no template.")
        
        # Ajouter output_type à self.args si spécifié
        if output_type:
            self.args["output_type"] = output_type

        # Compiler les enfants et les inclure dans le contexte
        # rendered_children = [child.compile(output_type) for child in self.children]
        self.args["children"] = self.children

        # Rendre le template avec le contexte
        rendered_content = self.template.render(self.args)
        return rendered_content
    
    def __str__(self):
        """
        Retourne une représentation en chaîne de la structure du nœud et de ses enfants.
        """
        # Format the current node's tag and attributes
        node_str = f"Node(tag='{self.tag}', args={self.args})"

        # Format the children recursively
        if self.children:
            children_str = "\n".join(["  " + str(child).replace("\n", "\n  ") for child in self.children])
            return f"{node_str}\nChildren:\n{children_str}"
        else:
            return node_str
