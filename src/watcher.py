import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Dossier contenant les templates et fichiers surveillés
WATCHED_DIRS = [os.path.join("src","jinja","templates")]

class FileChangeHandler(FileSystemEventHandler):

    def __init__(self, input_file):
        super().__init__()

        self.input_file = input_file

    def on_modified(self, event):
        """
        Détecte les modifications dans les fichiers et relance la commande `run`.
        """
        if any(event.src_path.endswith(ext) for ext in [".xml", ".json", ".jinja"]):
            print(f"\n🔄 Fichier modifié : {event.src_path}")
            print("🚀 Recompilation en cours...\n")
            subprocess.run(["python", "cli.py", "run", self.input_file])

def start_watching(input_file):
    """
    Démarre l'observateur pour surveiller les fichiers et dossiers.
    """
    observer = Observer()
    event_handler = FileChangeHandler(input_file)

    watched_dirs = WATCHED_DIRS + [input_file]

    for path in watched_dirs:
        observer.schedule(event_handler, path, recursive=True)

    print("👀 Surveillance des fichiers en cours... (CTRL+C pour arrêter)\n")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_watching()
