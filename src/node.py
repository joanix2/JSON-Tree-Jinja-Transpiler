import ast
from typing import List, Optional
from .templates_manager import TemplateManager

class Node(ast.AST):
    """
    Représente un nœud AST avec un `tag`, des `enfants`, et des `arguments` pour la compilation via Jinja.
    """

    def __init__(self, templates_manager: TemplateManager, tag: str, children: Optional[List["Node"]]=None, **args):
        """
        Initialise un nœud avec un tag, un template, des enfants, et des arguments supplémentaires.

        :param tag: Le nom de la balise.
        :param template: Le contenu du template (string).
        :param children: Une liste de nœuds enfants (par défaut, vide).
        :param args: Autres arguments passés pour le rendu du template.
        """
        self.tag = tag
        self.children = children or []
        self.templates_manager = templates_manager

        # Mapping automatique des arguments supplémentaires
        for key, value in args.items():
            setattr(self, key, value)

    def __getattr__(self, item):
        """
        Compile le template en ajoutant `compilation_mode` aux arguments et en rendant les enfants récursivement.

        :param compilation_mode: Le type de sortie à ajouter aux arguments (ex. 'html' ou 'css').
        :return: Le rendu du template sous forme de chaîne.
        """

        # Vérifie si le nœud a un template
        if not (item in self.templates_manager.get_templates_names(self.tag)):
            raise ValueError(f"Node '{self.tag}' cannot be compiled because it has no template '{item}'.")

        # Rendre le template avec le contexte
        return self.templates_manager.get_template(self.tag, item, self.__dict__)
    
    def __str__(self):
        """
        Retourne une représentation en chaîne de la structure du nœud et de ses enfants.
        """
        # Format the current node's tag and attributes
        node_str = f"Node(tag='{self.tag}', args={self.__dict__})"

        # Format the children recursively
        if self.children:
            children_str = "\n".join(["  " + str(child).replace("\n", "\n  ") for child in self.children])
            return f"{node_str}\nChildren:\n{children_str}"
        else:
            return node_str
