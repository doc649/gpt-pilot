# app/recipe_generator.py

"""
Module pour générer des recettes personnalisées
en fonction des ingrédients donnés par l'utilisateur.
Utilise OpenAI pour la génération créative.
"""

import os
import logging
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

# Chargement des variables d'environnement
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vérification de la clé
if not OPENAI_API_KEY:
    raise ValueError("La clé OPENAI_API_KEY n'est pas définie.")

# Initialisation du client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuration du logging
logger = logging.getLogger(__name__)

def format_ingredients(ingredients: List[str]) -> str:
    """Formate la liste des ingrédients pour l'injecter dans le prompt."""
    return ", ".join(ingredient.strip().lower() for ingredient in ingredients)

def generate_recipes(user_input: str) -> str:
    """
    Génère une recette à partir d'une liste d'ingrédients ou d'un thème donné.
    
    Args:
        user_input (str): Liste d'ingrédients ou thème envoyé par l'utilisateur.

    Returns:
        str: Recette générée
    """
    logger.info(f"Génération de recette pour: {user_input}")

    prompt = (
        "Tu es un grand chef étoilé. "
        "Génère une recette simple, rapide, et délicieuse "
        "basée uniquement sur ces ingrédients ou ce thème:\n\n"
        f"{user_input}\n\n"
        "Structure :\n"
        "- Nom du plat\n"
        "- Ingrédients (avec quantités approximatives)\n"
        "- Étapes détaillées de préparation\n"
        "- Astuce bonus de chef à la fin"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
        )
        recipe = response.choices[0].message.content.strip()
        logger.debug("Recette générée avec succès")
        return recipe

    except Exception as e:
        logger.error(f"Erreur lors de la génération de recette: {e}", exc_info=True)
        return "Désolé, une erreur est survenue lors de la création de votre recette."

