# app/openai_services.py

import os
import logging
import requests
from dotenv import load_dotenv
from typing import Optional
from openai import OpenAI
from app.recipe_generator import generate_recipes
from app.meal_planner import generate_meal_plan, estimate_calories, generate_shopping_list

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

def generate_help_message() -> str:
    """Message d'aide pour ChefBotDZ."""
    return (
        "📖 هاك واش تقدر تدير مع ChefBotDZ:\n"
        "- 🥘 طلب وصفة جزائرية حسب المكونات لي عندك\n"
        "- 🗓️ طلب بلان تاع الماكلة للأسبوع (plan repas)\n"
        "- 🛒 إنشاء ليستة تاع المقاضي (liste de courses)\n"
        "- 📸 صوّر واش عندك فالثلاجة وأنا نعطيك وصفة\n\n"
        "📥 أرسل المكونات ولا صورة تاع ثلاجتك، وChefBotDZ يعطيك وش تطيب!\n"
        "🔎 إذا حاب تعرف أكثر، أرسل: aide / help"
    )

def process_text(text: str) -> str:
    """
    Analyse la commande utilisateur et agit en fonction du besoin.
    """
    lower_text = text.lower()

    if "plan repas" in lower_text or "planning" in lower_text:
        return generate_meal_plan()
    elif "courses" in lower_text or "shopping" in lower_text or "liste" in lower_text:
        return generate_shopping_list(text)
    elif "calorie" in lower_text or "nutrition" in lower_text:
        return estimate_calories(text)
    elif "help" in lower_text or "aide" in lower_text or "/help" in lower_text:
        return generate_help_message()
    else:
        return generate_recipes(text)

def process_image(file_id: str) -> str:
    """
    Utilise GPT-4 Vision pour extraire les ingrédients d'une image et proposer des recettes.
    """
    logger.info(f"Traitement image file_id: {file_id}")
    file_path = get_file_path(file_id)
    if not file_path:
        return "❌ Impossible d'accéder à l'image envoyée."

    image_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Quels ingrédients reconnais-tu dans cette image ? Donne-moi uniquement les noms d'ingrédients séparés par des virgules."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ],
            max_tokens=300,
        )
        ingredients = response.choices[0].message.content.strip()
        return generate_recipes(ingredients)
    except Exception as e:
        logger.error(f"Erreur GPT-4 Vision: {e}")
        return f"Erreur lors de l'analyse de l'image: {str(e)}"

def get_file_path(file_id: str) -> Optional[str]:
    """
    Récupère le chemin d'un fichier Telegram pour l'analyser.
    """
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
