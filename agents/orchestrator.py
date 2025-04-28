# app/orchestrator.py

import time
import logging
from agents.agent import ProjectManager
from agents.watcher import watcher_loop

logger = logging.getLogger("Orchestrator")

class Orchestrator:
    def __init__(self):
        self.project_manager = ProjectManager()
    
    def supervise_project(self):
        logger.info("🧠 Orchestrator démarré pour supervision ChefBotDZ...")

        # 1. Analyse initiale du projet
        logger.info("📋 Analyse initiale du projet...")
        results = self.project_manager.analyze_project()

        # 2. Décision intelligente basée sur les résultats
        pilot_analysis = results.get("pilot_analysis", "")
        
        if "problème critique" in pilot_analysis.lower() or "erreur" in pilot_analysis.lower():
            logger.warning("🚨 Problème détecté dans le projet, correction prioritaire recommandée.")
        else:
            logger.info("✅ Aucun problème critique détecté, projet stable pour le moment.")

        # 3. Démarrage du Watcher pour surveillance continue
        logger.info("👁️ Activation du Watcher pour surveillance en temps réel...")
        time.sleep(2)
        watcher_loop()

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.supervise_project()
