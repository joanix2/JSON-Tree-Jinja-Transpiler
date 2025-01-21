# XML DSL Compiler Generator

Ce projet est un générateur de DSL qui convertit du code XML grâce à des templates Jinja. L'objectif est d'auto-générer les DSL, de créer des tests associés et d'adopter une philosophie de développement orientée tests (Test Driven Development), où ChatGPT aide à corriger les erreurs.

### Exemple d’utilisation dans le terminal :

1. Traiter un fichier XML avec les valeurs par défaut :

   ```bash
   python cli.py
   ```

2. Spécifier un fichier XML d’entrée :

   ```bash
   python cli.py custom_file.xml
   ```

3. Spécifier un fichier XML d’entrée et un répertoire de sortie personnalisé :
   ```bash
   python cli.py custom_file.xml --output-dir custom_output
   ```

### Bonnes pratiques :

1. **Utiliser un environnement virtuel** :

   - Créez un environnement virtuel pour isoler les dépendances de votre projet :
     ```bash
     python -m venv venv
     ```

2. **Réduire les dépendances inutiles** :

   - Évitez d’ajouter des dépendances inutiles au fichier `requirements.txt`. Nettoyez-le si nécessaire.

3. **Mettre à jour régulièrement** :
   - Si vous ajoutez de nouvelles bibliothèques, n'oubliez pas de régénérer le fichier :
     ```bash
     pip freeze > requirements.txt
     ```
