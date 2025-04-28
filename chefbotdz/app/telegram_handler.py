# app/telegram_handler.py

import os
import logging
import requests

from typing import Dict, Any, Optional, Union
from dotenv import load_dotenv
from chefbotdz.app.openai_services import process_text, process_image

# Ajout configuration logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configuration logging
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("La variable TELEGRAM_TOKEN est manquante.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def handle_update(update):
    logger.info(f"📥 Nouveau message reçu: {update.get('message', {}).get('text', '')}")

    if "message" not in update:
        return {"status": "no_message"}

    message = update["message"]
    chat_id = message["chat"]["id"]

    try:
        if "text" in message:
            user_text = message["text"]
            response_text = process_text(user_text)
            logger.info(f"🍳 Réponse générée pour le texte: {response_text}")
            send_message(chat_id, response_text)
            return {"status": "ok", "response": response_text}

        elif "photo" in message:
            file_id = message["photo"][-1]["file_id"]
            response_text = process_image(file_id)
            logger.info(f"🖼️ Réponse générée pour l'image: {response_text}")
            send_message(chat_id, response_text)
            return {"status": "ok", "response": response_text}

        else:
            logger.warning("Format non supporté reçu.")
            return {"status": "unsupported_format"}

    except Exception as e:
        logger.error(f"🚨 Erreur lors du traitement du message: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}

def send_message(chat_id: Union[int, str], text: str) -> Dict[str, Any]:
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"Erreur envoi message: {e}")
        return {"ok": False, "error": str(e)}

def send_chat_action(chat_id: Union[int, str], action: str) -> Dict[str, Any]:
    url = f"{TELEGRAM_API_URL}/sendChatAction"
    payload = {"chat_id": chat_id, "action": action}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"Erreur chat action: {e}")
        return {"ok": False, "error": str(e)}

def start_bot() -> int:
    logger.info("Bot prêt à être connecté via webhook ou polling...")
    # À implémenter selon ta méthode de lancement
    return 0
