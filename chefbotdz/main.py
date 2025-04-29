# main.py
# redeploy trigger

from flask import Flask, request, jsonify
from app.telegram_handler import handle_update
from app.config import TELEGRAM_TOKEN
from app.telegram_handler import logger
from app.db import initialize_database  # 👈 Initialiser la DB
import os
import requests

app = Flask(__name__)

# 🚀 Fonction pour configurer automatiquement le webhook
def setup_webhook():
    BASE_URL = os.getenv("RENDER_EXTERNAL_URL", "https://chefbot-dz.onrender.com")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "chefbotsecret")
    webhook_url = f"{BASE_URL}/webhook"
    set_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"

    payload = {
        "url": webhook_url,
        "secret_token": WEBHOOK_SECRET
    }

    try:
        response = requests.post(set_webhook_url, json=payload)
        if response.status_code == 200:
            logger.info("✅ Webhook Telegram configuré avec succès !")
        else:
            logger.error(f"❌ Erreur configuration Webhook : {response.text}")
    except Exception as e:
        logger.error(f"❌ Exception lors de la configuration Webhook: {str(e)}")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    logger.info(f"🔔 Webhook reçu: {update}")
    result = handle_update(update)
    return jsonify({
        "status": "success",
        "processed": True,
        "details": result
    })

if __name__ == "__main__":
    initialize_database()  # 👈 On initialise la base
    setup_webhook()        # 👈 On configure le webhook Telegram
    app.run(host="0.0.0.0", port=5000, debug=True)


# app/config.py
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_ID = os.getenv("ADMIN_ID")


# app/telegram_handler.py
import requests
from flask import jsonify
from app.openai_services import process_text, process_image
from app.config import TELEGRAM_TOKEN, ADMIN_ID

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def handle_update(update):
    if "message" not in update:
        return jsonify({"status": "no message"})

    message = update["message"]
    chat_id = message["chat"]["id"]

    if "text" in message:
        response = process_text(message["text"])
        send_message(chat_id, response)

    elif "photo" in message:
        file_id = message["photo"][-1]["file_id"]  # get highest quality image
        response = process_image(file_id)
        send_message(chat_id, response)

    return jsonify({"status": "ok"})


def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })


# app/openai_services.py
import openai
import requests
from app.config import OPENAI_API_KEY, TELEGRAM_TOKEN
from app.recipe_generator import generate_recipes
from app.meal_planner import generate_meal_plan, estimate_calories, generate_shopping_list

openai.api_key = OPENAI_API_KEY

def process_text(text):
    if "plan repas" in text.lower():
        return generate_meal_plan()
    elif "courses" in text.lower():
        return generate_shopping_list(text)
    elif "calorie" in text.lower():
        return estimate_calories(text)
    else:
        return generate_recipes(text)

def process_image(file_id):
    # Get Telegram file URL
    file_path = get_file_path(file_id)
    if not file_path:
        return "Impossible de récupérer l'image."
    image_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"

    # GPT-4 Vision API call
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Quels ingrédients reconnais-tu dans cette image ? Donne-moi uniquement les noms d'ingrédients, séparés par des virgules."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ],
            max_tokens=300
        )
        ingredients = response.choices[0].message.content.strip()
        return generate_recipes(ingredients)
    except Exception as e:
        return f"Erreur lors de l'analyse de l'image : {str(e)}"

def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
    try:
        r = requests.get(url)
        file_path = r.json()["result"]["file_path"]
        return file_path
    except:
        return None


# app/recipe_generator.py
def generate_recipes(ingredients):
    return f"Voici des idées de plats algériens à base de : {ingredients}\n\n1. Chakchouka\n2. Tajine jelbana\n3. Batata mchermla"


# app/meal_planner.py
def generate_meal_plan():
    return "🗓️ Plan repas 7 jours :\nLundi: Rechta\nMardi: Couscous\nMercredi: Chakhchoukha\n..."

def estimate_calories(recipe_text):
    return "Cette recette est estimée à environ 450 kcal par portion."

def generate_shopping_list(text):
    return "🛒 Liste de courses :\n- Pommes de terre\n- Tomates\n- Oeufs"