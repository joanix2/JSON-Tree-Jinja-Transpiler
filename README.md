# XML DSL Compiler Generator

Ce projet est un générateur de DSL qui convertit du code XML grâce à des templates Jinja. L'objectif est d'auto-générer les DSL, de créer des tests associés et d'adopter une philosophie de développement orientée tests (Test Driven Development), où ChatGPT aide à corriger les erreurs.

## Commandes disponibles

1. **`compile`**  
   Traite un fichier XML et génère des fichiers à partir de templates.

   **Exemples d’utilisation :**

   - Traiter un fichier XML avec les valeurs par défaut (fichier `main.xml` dans le répertoire courant) et générer les fichiers dans `output/` :

     ```bash
     python cli.py compile
     ```

   - Spécifier un fichier XML d’entrée personnalisé :

     ```bash
     python cli.py compile custom_file.xml
     ```

   - Spécifier un fichier XML d’entrée et un répertoire de sortie personnalisé :
     ```bash
     python cli.py compile custom_file.xml --output-dir custom_output
     ```

2. **`build`**  
   Génère une arborescence de projet à partir d’un fichier de configuration YAML.

   **Exemples d’utilisation :**

   - Générer une arborescence en utilisant le fichier YAML par défaut (`infrastructure.yml`) :

     ```bash
     python cli.py build
     ```

   - Spécifier un fichier YAML de configuration différent :
     ```bash
     python cli.py build --config-file custom_config.yml
     ```

3. **`generate tests`**
   **Générer des tests avec les valeurs par défaut :**

   ```bash
   python cli.py generate-tests
   ```

   **Spécifier un fichier XML d’entrée et un répertoire de sortie personnalisé :**

   ```bash
   python cli.py generate-tests custom_file.xml --output-dir custom_tests
   ```

   **Lister les commandes disponibles :**

   ```bash
   python cli.py --help
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

---

### Commande Docker pour créer un conteneur MongoDB

Vous pouvez exécuter la commande suivante pour lancer un conteneur MongoDB :

```bash
docker run -d --name mongodb-container \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo
```

#### Explications :

- `-d` : Lance le conteneur en arrière-plan (mode détaché).
- `--name mongodb-container` : Nomme le conteneur.
- `-p 27017:27017` : Expose le port 27017 (le port par défaut de MongoDB) du conteneur sur l'hôte.
- `-e MONGO_INITDB_ROOT_USERNAME=admin` : Définit l'utilisateur administrateur.
- `-e MONGO_INITDB_ROOT_PASSWORD=password` : Définit le mot de passe administrateur.
- `mongo` : Utilise l'image officielle MongoDB.

---
