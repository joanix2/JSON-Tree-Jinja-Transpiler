# XML DSL Compiler Generator

Ce projet est un générateur de DSL qui convertit du code **XML** grâce à des templates **Jinja**.  
L'objectif est **d’auto-générer des DSL**, de créer les tests associés et d’adopter une **philosophie de développement orientée tests** (Test Driven Development), où des **LLMs** aident à corriger les erreurs.

---

## 🚀 **Démarrage rapide**

📌 **Exécuter toutes les étapes automatiquement avec une seule commande** :

```bash
python cli.py run
```

🔹 **Que fait cette commande ?**

1. Vérifie si le fichier est au format **XML** ou **JSON**.
2. Si le fichier est XML, il est converti en JSON.
3. Le JSON est **parsé et validé**.
4. Si tout est correct, **l’arborescence de projet** est générée à partir du fichier YAML.

---

## 📌 **Commandes disponibles**

### **1️⃣ `run` (exécution complète)**

Exécute **toutes les étapes** automatiquement en une seule commande.

**Exemple d’utilisation :**

```bash
python cli.py run input.xml
```

ou avec un fichier JSON :

```bash
python cli.py run input.json
```

---

### **2️⃣ `compile` (traitement manuel du JSON)**

Traite un fichier **JSON** et génère les fichiers à partir de templates.

**Exemples d’utilisation :**

- **Par défaut**, traite `main.json` et génère les fichiers dans `output/` :

  ```bash
  python cli.py compile
  ```

- **Avec un fichier JSON personnalisé** :

  ```bash
  python cli.py compile custom_file.json
  ```

- **Avec un fichier JSON et un répertoire de sortie personnalisé** :
  ```bash
  python cli.py compile custom_file.json --output custom_output
  ```

---

### **3️⃣ `convert` (conversion XML → JSON uniquement)**

Convertit un fichier **XML** en **JSON** sans exécuter d’autres étapes.

**Exemples d’utilisation :**

- **Convertir un fichier XML en JSON avec le même nom** :

  ```bash
  python cli.py convert input.xml
  ```

  📌 **Sortie** : `input.json`

- **Convertir un fichier XML et spécifier un fichier de sortie JSON** :
  ```bash
  python cli.py convert input.xml --json-file custom_output.json
  ```

---

### **4️⃣ `build` (génération d’arborescence à partir du YAML)**

Génère une arborescence de projet en fonction d’un fichier **YAML**.

**Exemples d’utilisation :**

- **Générer une arborescence avec le fichier YAML par défaut** :

  ```bash
  python cli.py build
  ```

- **Utiliser un fichier YAML spécifique** :
  ```bash
  python cli.py build --config-file custom_config.yml
  ```

---

## ✅ **Bonnes pratiques**

### 1️⃣ **Utiliser un environnement virtuel**

Pour isoler les dépendances du projet :

```bash
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate  # Windows
```

### 2️⃣ **Installer les dépendances**

```bash
pip install -r requirements.txt
```

### 3️⃣ **Mettre à jour les dépendances**

Si vous ajoutez une nouvelle bibliothèque :

```bash
pip freeze > requirements.txt
```

---

## 📌 **Résumé des commandes principales**

| Commande                           | Action                                    |
| ---------------------------------- | ----------------------------------------- |
| `python cli.py run input.xml`      | Exécute toutes les étapes automatiquement |
| `python cli.py convert input.xml`  | Convertit XML → JSON                      |
| `python cli.py compile input.json` | Parse JSON et génère des fichiers         |
| `python cli.py build`              | Génère l’arborescence à partir d’un YAML  |

🚀 **Avec `run`, tout est automatisé !**

---