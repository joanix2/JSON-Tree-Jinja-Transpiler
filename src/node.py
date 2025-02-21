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
        self.args = args
        self.args["children"] = children if children else []

    def __getattr__(self, item):
        """
        Compile le template en ajoutant `compilation_mode` aux arguments et en rendant les enfants récursivement.

        :param compilation_mode: Le type de sortie à ajouter aux arguments (ex. 'html' ou 'css').
        :return: Le rendu du template sous forme de chaîne.
        """
        # Vérifie si le nœud a un template
        if not self.template:
            raise ValueError(f"Node '{self.tag}' cannot be compiled because it has no template.")
        
        # Ajouter compilation_mode à self.args si spécifié
        if item:
            self.args["compilation_mode"] = item

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
