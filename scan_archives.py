import os
import json

# --- Configuration ---
START_DIR = 'archives'  # Le dossier à scanner
OUTPUT_FILE = 'structure.json'  # Le nom du fichier JSON de sortie

def scan_directory(current_path):
    """
    Fonction récursive pour scanner un répertoire et construire la structure.
    
    Args:
        current_path (str): Le chemin du répertoire actuel.
        
    Returns:
        list: La structure d'objets (JSON) représentant les fichiers et dossiers.
    """
    items = []
    
    try:
        # Liste tous les fichiers et dossiers dans le chemin actuel
        directory_contents = os.listdir(current_path)
    except FileNotFoundError:
        print(f"Erreur : Le répertoire '{current_path}' est introuvable.")
        return []
        
    # Parcours des éléments
    for item_name in directory_contents:
        full_item_path = os.path.join(current_path, item_name)
        
        if os.path.isdir(full_item_path):
            # C'est un dossier
            children = scan_directory(full_item_path)
            items.append({
                'name': item_name,
                'type': 'folder',
                'children': children
            })
        elif os.path.isfile(full_item_path):
            # C'est un fichier
            # On utilise le chemin Unix pour l'URL (remplacement des '\' par des '/')
            relative_path_for_url = full_item_path.replace(os.sep, '/')
            items.append({
                'name': item_name,
                'type': 'file',
                'path': relative_path_for_url
            })

    # Triage : Les dossiers en premier, puis les fichiers, par ordre alphabétique
    items.sort(key=lambda x: (x['type'] != 'folder', x['name']))
    
    return items

# --- Exécution du script ---
if __name__ == '__main__':
    print(f"Démarrage du scan du dossier : {START_DIR}")
    
    # Construction de la structure
    file_structure = scan_directory(START_DIR)
    
    # Écriture du fichier JSON
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # indent=2 formate le JSON avec 2 espaces pour la lisibilité
            json.dump(file_structure, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Structure JSON générée avec succès : {OUTPUT_FILE}")
        print("N'oubliez pas de commiter ce fichier JSON (et le script) sur GitHub !")
        
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier JSON : {e}")
