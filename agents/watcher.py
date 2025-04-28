# watcher.py

import os
import time
import json
from datetime import datetime
from agents.agent import ProjectManager

# Dossiers et extensions à surveiller
WATCHED_DIRS = ["./ChefBotDZ", "./modules", "./core", "."]
WATCHED_EXTENSIONS = [".py"]
ANALYSIS_INTERVAL = 3600  # 1h pour l'analyse automatique

# Dossiers résultats
RESULTS_DIR = "./analysis_results"
LOG_FILE = os.path.join(RESULTS_DIR, "watcher_log.txt")
os.makedirs(RESULTS_DIR, exist_ok=True)

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_message = f"[{timestamp}] {message}"
    print(final_message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(final_message + "\n")

def snapshot_files():
    snapshot = {}
    for folder in WATCHED_DIRS:
        if os.path.exists(folder):
            for root, _, files in os.walk(folder):
                for file in files:
                    if any(file.endswith(ext) for ext in WATCHED_EXTENSIONS):
                        path = os.path.join(root, file)
                        snapshot[path] = os.path.getmtime(path)
    return snapshot

def run_analysis(changed_files=None):
    log("🧠 Lancement d'une analyse du projet...")
    pm = ProjectManager()
    if changed_files:
        results = []
        for file in changed_files:
            log(f"📄 Analyse du fichier modifié: {file}")
            results.append(pm.analyze_specific_file(file))
    else:
        results = pm.analyze_project()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = os.path.join(RESULTS_DIR, f"analysis_{timestamp}.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    log(f"✅ Résultats enregistrés dans {results_path}")

def watcher_loop():
    log("👁️ Watcher en route...")
    last_snapshot = snapshot_files()
    last_analysis = time.time()

    try:
        while True:
            time.sleep(2)
            current_snapshot = snapshot_files()
            changed = [
                file for file in set(last_snapshot) | set(current_snapshot)
                if current_snapshot.get(file) != last_snapshot.get(file)
            ]

            if changed:
                log(f"🔁 Modifications détectées sur {len(changed)} fichier(s)")
                run_analysis(changed)

                last_snapshot = current_snapshot
                last_analysis = time.time()

            elif time.time() - last_analysis > ANALYSIS_INTERVAL:
                log("⏰ Analyse globale planifiée")
                run_analysis()
                last_analysis = time.time()

    except KeyboardInterrupt:
        log("🛑 Watcher arrêté manuellement.")

if __name__ == "__main__":
    watcher_loop()
