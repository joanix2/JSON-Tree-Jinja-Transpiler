import xml.etree.ElementTree as ET
import json

def xml_to_dict(element):
    """Convertit un élément XML en un dictionnaire JSON structuré."""
    node = {"tag": element.tag}
    
    # Ajoute les attributs s'ils existent
    if element.attrib:
        node["attributes"] = element.attrib

    # Ajoute les enfants récursivement
    children = [xml_to_dict(child) for child in element]
    if children:
        node["children"] = children
    
    # Si l'élément a du texte non vide, on l'ajoute sous "value"
    text = element.text.strip() if element.text and element.text.strip() else None
    if text:
        node["value"] = text

    return node

def convert_xml_to_json(xml_file, json_file):
    """Convertit un fichier XML en fichier JSON."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    json_data = xml_to_dict(root)
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print(f"Conversion terminée. Résultat enregistré dans {json_file}")
