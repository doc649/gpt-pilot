# app/recipe_generator.py

"""
Module pour générer des suggestions de recettes algériennes personnalisées
basées sur des ingrédients donnés. Retourne 1 à 3 options.
Langue principale : darija algérienne en lettres arabes + français simple si nécessaire.
"""

import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Chargement des variables d'environnement
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("La clé OPENAI_API_KEY n'est pas définie.")

# Initialisation du client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuration logging
logger = logging.getLogger(__name__)

def generate_recipes(user_ingredients_text: str) -> list:
    """
    Génère 1 à 3 suggestions de recettes DZ basées sur les ingrédients donnés.

    Args:
        user_ingredients_text (str): Ingrédients envoyés par l'utilisateur.

    Returns:
        list: Liste de 1 à 3 recettes courtes prêtes à être proposées.
    """
    logger.info(f"🧠 Génération de suggestions de recettes pour: {user_ingredients_text}")

    # Prompt blindé DZ
    prompt = f"""
أنت ChefBotDZ، طباخ جزائري ذكي.

🎯 المطلوب :
- اقترح على المستخدم 1 إلى 3 وصفات جزائرية حقيقية تناسب المكونات لي عطاهم.
- كل وصفة لازم تكون عبارة عن عنوان قصير مع وصف صغير (سطرين بالكثير).
- استعمل الدارجة الجزائرية بالحروف العربية. وإذا كان لازم، زيد كلمة تقنية بالفرنسية بين قوسين.
- إذا المكونات قليلة بزاف وماكاش وصفات معروفة، اقترح إضافة مكون واحد فقط.
- جاوب بدون مقدمات طويلة، دخل ديريكت فالعرض.

🎯 المكونات :
{user_ingredients_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_ingredients_text}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        raw_text = response.choices[0].message.content.strip()
        logger.info("✅ Suggestions de recettes générées avec succès")

        # Découper la réponse en 1-3 recettes
        suggestions = [line.strip() for line in raw_text.split('\n') if line.strip()]
        return suggestions[:3]  # Prendre maximum 3 recettes

    except Exception as e:
        logger.error(f"🚨 Erreur lors de la génération de suggestions: {e}", exc_info=True)
        return ["❌ خطأ وقع أثناء توليد الوصفة، حاول مرة أخرى."]
