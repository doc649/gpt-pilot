import os
from openai import OpenAI
from dotenv import load_dotenv

# Charge la clé API depuis le fichier .env ou les variables d'environnement
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialisation du client OpenAI
client = OpenAI(api_key=openai_api_key)

# Tâche claire pour GPT Pilot : génération de recette
def generate_recipe(prompt):
    print("🔧 Génération de recette avec GPT...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur lors de l'appel à GPT : {e}"

# Exemple de prompt
recipe_prompt = "Donne-moi une recette simple et rapide de pain perdu."

# Appel à la fonction
if __name__ == "__main__":
    print("🚀 Exécution de run_gpt_pilot.py")
    result = generate_recipe(recipe_prompt)
    print("\n📋 Résultat :\n")
    print(result)
