#!/usr/bin/env python

"""
ChefBotDZ - Main Entry
Bot Telegram IA : Planification de repas et recettes intelligentes.
Version avec Orchestrator, Agents GPT (Pilot, Watcher) et Watcher Intelligent.
"""

import os
import sys
import argparse
import logging
from typing import Optional

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chefbotdz.log")
    ]
)
logger = logging.getLogger("ChefBotDZ")

def check_environment() -> bool:
    """Vérifie les dépendances et variables essentielles."""
    try:
        import dotenv
        import openai
        import requests
        
        dotenv.load_dotenv()
        required_vars = ["TELEGRAM_TOKEN", "OPENAI_API_KEY"]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            logger.error(f"Variables d'environnement manquantes : {', '.join(missing)}")
            return False
        return True
    except ImportError as e:
        logger.error(f"Module manquant : {e.name}")
        return False

def setup_structure() -> None:
    """Création des dossiers du projet si besoin."""
    folders = ["logs", "data", "modules", "tests", "analysis_results"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        logger.debug(f"Dossier vérifié/créé : {folder}")

def parse_arguments() -> argparse.Namespace:
    """Parse les arguments du terminal."""
    parser = argparse.ArgumentParser(description="ChefBotDZ - Bot IA pour la nutrition")
    parser.add_argument("--debug", action="store_true", help="Mode Debug activé")
    parser.add_argument("--mode", choices=["bot", "agent", "watcher", "orchestrator"], default="bot",
                        help="Mode de lancement : bot | agent | watcher | orchestrator")
    return parser.parse_args()

def run_bot() -> int:
    """Démarre le Bot Telegram."""
    try:
        from app.telegram_handler import start_bot
        logger.info("🚀 Démarrage du Bot Telegram...")
        return start_bot()
    except Exception as e:
        logger.exception(f"Erreur lancement Bot : {e}")
        return 1

def run_agent() -> int:
    """Lance l'analyse du code par les agents Pilot/Watcher."""
    try:
        from app.agent import ProjectManager
        logger.info("🧠 Lancement des Agents Pilot/Watcher...")
        manager = ProjectManager()
        manager.analyze_project()
        return 0
    except Exception as e:
        logger.exception(f"Erreur lancement Agents : {e}")
        return 1

def run_watcher() -> int:
    """Surveille les fichiers pour déclencher l'analyse automatique."""
    try:
        from app.watcher import watcher_loop
        logger.info("👁️ Watcher en cours...")
        watcher_loop()
        return 0
    except Exception as e:
        logger.exception(f"Erreur Watcher : {e}")
        return 1

def run_orchestrator() -> int:
    """Coordonne Pilot, Watcher et Automation."""
    try:
        from app.orchestrator import orchestrator_loop
        logger.info("🛠️ Orchestrator actif : coordination intelligente...")
        orchestrator_loop()
        return 0
    except Exception as e:
        logger.exception(f"Erreur Orchestrator : {e}")
        return 1

def main() -> int:
    """Point d'entrée principal."""
    args = parse_arguments()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Mode Debug ON")
    
    if not check_environment():
        logger.error("Problème environnement ❌")
        return 255

    setup_structure()

    if args.mode == "bot":
        return run_bot()
    elif args.mode == "agent":
        return run_agent()
    elif args.mode == "watcher":
        return run_watcher()
    elif args.mode == "orchestrator":
        return run_orchestrator()
    else:
        logger.error(f"Mode inconnu : {args.mode}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("⛔ Interruption par l'utilisateur.")
        sys.exit(0)
