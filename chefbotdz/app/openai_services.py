# app/openai_services.py

import os
import logging
import requests
from dotenv import load_dotenv
from typing import Optional
from openai import OpenAI

# Configuration logging
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_TOKEN:
    raise ValueError("Clés API manquantes. Vérifiez votre .env.")

# Initialisation client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def process_text(text: str) -> str:
    """Analyse le texte utilisateur et agit."""
    logger.info(f"Traitement texte: {text[:50]}...")
    if any(k in text.lower() for k in ["plan repas", "planning"]):
        return "🗓️ Je vais générer un plan de repas personnalisé."
    elif any(k in text.lower() for k in ["courses", "shopping", "liste"]):
        return "🛒 Voici votre liste de courses générée."
    elif any(k in text.lower() for k in ["calorie", "nutrition"]):
        return "🍎 Estimation nutritionnelle en cours."
    elif any(k in text.lower() for k in ["aide", "help"]):
        return generate_help_message()
    else:
        return f"🍳 Proposition de recette basée sur: {text}"

def process_image(file_id: str) -> str:
    """Utilise GPT-4 Vision pour extraire les ingrédients d'une image."""
    logger.info(f"Traitement image file_id: {file_id}")
    file_path = get_file_path(file_id)
    if not file_path:
        return "Erreur: Impossible d'accéder à l'image."

    image_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Quels ingrédients reconnais-tu dans cette image ?"},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=300,
        )
        ingredients = response.choices[0].message.content.strip()
        return f"🍅 Ingrédients reconnus : {ingredients}"
    except Exception as e:
        logger.error(f"Erreur GPT-4 Vision: {e}")
        return f"Erreur lors de l'analyse de l'image: {str(e)}"

def get_file_path(file_id: str) -> Optional[str]:
    """Récupère le chemin d'un fichier Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile"
    try:
        r = requests.post(url, json={"file_id": file_id})
        r.raise_for_status()
        result = r.json()
        if result.get("ok"):
            return result["result"]["file_path"]
        return None
    except Exception as e:
        logger.error(f"Erreur récupération file path: {e}")
        return None

def generate_help_message() -> str:
    """Message d'aide aux utilisateurs."""
    return ("📖 Commandes disponibles:\n"
            "- Plan de repas personnalisé\n"
            "- Estimation nutritionnelle\n"
            "- Génération de liste de courses\n"
            "- Lecture d'ingrédients via photo\n")
