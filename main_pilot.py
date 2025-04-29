#!/usr/bin/env python

"""
ChefBotDZ - Main Entry
Bot Telegram IA : Planification de repas et recettes DZ intelligentes.
Version avec Orchestrator, Agents GPT (Pilot, Watcher) et Watcher Intelligent.
"""

# 📦 Imports standards
import os
import sys
import argparse
import logging
from typing import Optional

# 📦 Imports packages externes
import dotenv
import openai
import requests

# ✅ Ajouter les bons chemins
sys.path.append(os.path.abspath("chefbotdz"))
sys.path.append(os.path.abspath("agents"))

# 📦 Imports internes projet
from agents.agent import ProjectManager
from agents.watcher import watcher_loop
from agents.orchestrator import Orchestrator

# 🔧 Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chefbotdz.log")
    ]
)
logger = logging.getLogger("ChefBotDZ")

# 🔧 Chargement de l'environnement
dotenv.load_dotenv()

# ✅ Fonctions utilitaires

def check_environment() -> bool:
    """Vérifie la présence des variables nécessaires."""
    required_vars = ["TELEGRAM_TOKEN", "OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.error(f"❌ Variables d'environnement manquantes : {', '.join(missing)}")
        return False
    return True

def setup_structure() -> None:
    """Crée les dossiers nécessaires au fonctionnement."""
    folders = ["logs", "data", "analysis_results"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        logger.debug(f"Dossier vérifié/créé : {folder}")

def parse_arguments() -> argparse.Namespace:
    """Récupère les arguments de lancement."""
    parser = argparse.ArgumentParser(description="ChefBotDZ - Bot IA DZ")
    parser.add_argument("--debug", action="store_true", help="Activer le mode debug")
    parser.add_argument("--mode", choices=["bot", "agent", "watcher", "orchestrator"], default="bot",
                        help="Choisir le mode de lancement : bot | agent | watcher | orchestrator")
    return parser.parse_args()

# 🚀 Fonctions principales

def run_bot() -> int:
    """Démarre le bot Telegram."""
    try:
        from app.telegram_handler import start_bot
        logger.info("🤖 Lancement du bot Telegram...")
        return start_bot()
    except Exception as e:
        logger.exception(f"🚨 Erreur démarrage Bot : {e}")
        return 1

def run_agent() -> int:
    """Exécute l’analyse du projet via Pilot + Watcher."""
    try:
        logger.info("🧠 Agents Pilot & Watcher en action...")
        manager = ProjectManager()
        manager.analyze_project()
        return 0
    except Exception as e:
        logger.exception(f"🚨 Erreur Agent : {e}")
        return 1

def run_watcher() -> int:
    """Surveille les fichiers pour détecter des modifications."""
    try:
        logger.info("👁️ Watcher actif...")
        watcher_loop()
        return 0
    except Exception as e:
        logger.exception(f"🚨 Erreur Watcher : {e}")
        return 1

def run_orchestrator() -> int:
    """Coordonne intelligemment Pilot, Watcher et corrections."""
    try:
        logger.info("🛠️ Orchestrator lancé...")
        orchestrator = Orchestrator()
        orchestrator.supervise_project()
        return 0
    except Exception as e:
        logger.exception(f"🚨 Erreur Orchestrator : {e}")
        return 1

# 🎯 Point d’entrée principal

def main() -> int:
    args = parse_arguments()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("🛠️ Mode DEBUG activé")

    if not check_environment():
        logger.error("❌ Problème dans la configuration .env")
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
        logger.error(f"🚫 Mode de lancement inconnu : {args.mode}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("⛔ Interruption manuelle détectée.")
        sys.exit(0)
