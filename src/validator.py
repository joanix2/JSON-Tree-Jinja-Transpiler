import os
import jsonschema
from jsonschema import validate
from .utils import load_file

# Fonction de validation
def validate_json(data, schema):
    """Valide un JSON selon un schéma JSON."""
    try:
        validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print("❌ JSON invalide :", e.message)
        return False
    
# Vérifier la structure global
def check_tree(json_data):
    # JSON Schema pour une structure en arbre
    node_schema_path = os.path.join(os.path.dirname(__file__), "assets", "tree_schema.json")
    node_schema = load_file(node_schema_path)

    # Exécuter la validation
    return validate_json(json_data, node_schema)
    
# Vérifier que chaque nœud correspond bien au schéma défini pour son `tag`.

# S'assurer que chaque template Jinja correspond au JSON Schema associé.