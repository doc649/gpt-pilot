# app/telegram_handler.py

import requests
import json
from flask import jsonify
from app.openai_services import process_text, process_image
from app.config import TELEGRAM_TOKEN
from app.db import add_user, get_user, increment_user_recipe_count, save_pending_recipes, get_pending_recipes, delete_pending_recipes
from app.recipe_generator import generate_recipes  # À ajuster si besoin
import logging

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Configuration logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def handle_update(update):
    if "message" not in update:
        return jsonify({"status": "no_message"})

    message = update["message"]
    chat_id = str(message["chat"]["id"])  # toujours en string pour la DB

    # 1️⃣ Enregistrer l'utilisateur s'il est nouveau
    add_user(chat_id)
    user = get_user(chat_id)

    if "text" in message:
        user_text = message["text"]

        # 2️⃣ Vérifier s'il est en train de choisir une recette
        pending = get_pending_recipes(chat_id)
        if pending:
            try:
                choice = int(user_text.strip())
                recipes = json.loads(pending["recipes"])

                if 1 <= choice <= len(recipes):
                    selected_recipe = recipes[choice - 1]
                    send_message(chat_id, selected_recipe)
                    delete_pending_recipes(chat_id)
                    return jsonify({"status": "recipe_sent"})
                else:
                    send_message(chat_id, "❌ رقم غير صالح. اختار بين 1 و 3.")
                    return jsonify({"status": "invalid_choice"})

            except ValueError:
                send_message(chat_id, "❌ أرسل رقم صالح (1 أو 2 أو 3).")
                return jsonify({"status": "invalid_choice"})

        # 3️⃣ Sinon ➔ normal process : vérifier quota utilisateur
        if not user["is_premium"] and user["recipes_today"] >= 3:
            send_message(chat_id, "🔒 لقد وصلت للحد المجاني 3 وصفات في اليوم.\n🎯 اشترك في النسخة Premium للحصول على وصفات غير محدودة !")
            return jsonify({"status": "limit_reached"})

        # 4️⃣ Générer 1-3 recettes possibles
        recipe_options = generate_recipes(user_text)  # retourne une liste de 1-3 recettes

        if isinstance(recipe_options, list) and len(recipe_options) > 1:
            options_text = "\n".join([f"{i+1}. {recipe}" for i, recipe in enumerate(recipe_options)])
            send_message(chat_id, f"🧑‍🍳 هاك بعض الاقتراحات:\n{options_text}\n\n📥 رد عليا بالرقم تاع الوصفة لي تحبها (1 أو 2 أو 3).")
            save_pending_recipes(chat_id, json.dumps(recipe_options))
        else:
            send_message(chat_id, recipe_options[0])

        # 5️⃣ Incrémenter le compteur si utilisateur Freemium
        if not user["is_premium"]:
            increment_user_recipe_count(chat_id)

        return jsonify({"status": "ok"})

    elif "photo" in message:
        file_id = message["photo"][-1]["file_id"]  # meilleure qualité
        ingredients = process_image(file_id)

        recipe_options = generate_recipes(ingredients)

        if isinstance(recipe_options, list) and len(recipe_options) > 1:
            options_text = "\n".join([f"{i+1}. {recipe}" for i, recipe in enumerate(recipe_options)])
            send_message(chat_id, f"🧑‍🍳 هاك بعض الاقتراحات:\n{options_text}\n\n📥 رد عليا بالرقم تاع الوصفة لي تحبها (1 أو 2 أو 3).")
            save_pending_recipes(chat_id, json.dumps(recipe_options))
        else:
            send_message(chat_id, recipe_options[0])

        # 5️⃣ Incrémenter le compteur si utilisateur Freemium
        if not user["is_premium"]:
            increment_user_recipe_count(chat_id)

        return jsonify({"status": "ok"})

    return jsonify({"status": "unsupported_format"})
