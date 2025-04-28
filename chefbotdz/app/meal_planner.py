# app/meal_planner.py

"""
Module pour la génération rapide de :
- Plan de repas sur 7 jours
- Estimation des calories
- Liste de courses basique
Spécialement optimisé pour réponses Telegram (<400 tokens).
"""

import random

# Plans de repas par défaut
DEFAULT_MEALS = [
    "Rechta",
    "Couscous",
    "Chakhchoukha",
    "Tajine zitoune",
    "Mhajeb",
    "Dolma",
    "Mhadjeb gratinés"
]

# Ingrédients génériques pour liste de courses
BASIC_INGREDIENTS = [
    "Pommes de terre", "Tomates", "Oignons", "Ail", 
    "Poivrons", "Carottes", "Poulet", "Œufs", 
    "Semoule", "Lait", "Farine", "Yaourt"
]

def generate_meal_plan() -> str:
    """
    Génère un plan de repas rapide sur 7 jours.
    
    Returns:
        str: Plan formaté prêt à envoyer.
    """
    random.shuffle(DEFAULT_MEALS)  # Mélanger pour varier
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    plan = "\n".join([f"{day}: {meal}" for day, meal in zip(days, DEFAULT_MEALS)])
    return f"🗓️ Plan repas 7 jours :\n{plan}"

def estimate_calories(recipe_text: str) -> str:
    """
    Estime rapidement les calories d'une recette simple.
    
    Args:
        recipe_text (str): Texte de la recette.
        
    Returns:
        str: Estimation de calories.
    """
    keywords = recipe_text.lower()
    base = 350  # base pour une recette moyenne
    
    # Pondérer selon ingrédients clés
    if "poulet" in keywords:
        base += 100
    if "fromage" in keywords or "gratin" in keywords:
        base += 150
    if "crème" in keywords:
        base += 200
    if "légumes" in keywords or "salade" in keywords:
        base -= 50
    
    return f"🔢 Estimation : environ {base} kcal par portion."

def generate_shopping_list(user_text: str) -> str:
    """
    Génère une liste de courses basique en fonction d'un texte utilisateur.
    
    Args:
        user_text (str): Demande utilisateur (exemple: "je veux cuisiner du couscous")
        
    Returns:
        str: Liste de courses prête.
    """
    items = list(BASIC_INGREDIENTS)

    # Ajouter des éléments spécifiques selon l'intention utilisateur
    lower_text = user_text.lower()
    if "couscous" in lower_text:
        items += ["Semoule fine", "Pois chiches", "Viande d'agneau"]
    if "rechta" in lower_text:
        items += ["Pâtes Rechta", "Poulet", "Pois chiches"]
    if "chakhchoukha" in lower_text:
        items += ["Galette sèche", "Sauce rouge", "Viande"]
    
    unique_items = sorted(set(items))  # Éviter doublons

    list_text = "\n- ".join(unique_items)
    return f"🛒 Liste de courses suggérée :\n- {list_text}"
