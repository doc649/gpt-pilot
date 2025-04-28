# agent.py

import os
import glob
import json
from openai import OpenAI
from dotenv import load_dotenv

# Charger la clé API
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Contexte global pour guider les réponses
PROJECT_CONTEXT = """
Projet: ChefBotDZ - Bot Telegram pour recettes et planification de repas.
Objectifs:
- Refactorisation
- Sécurité
- Tests
- Améliorations IA
- Interface utilisateur Flask
"""

ROADMAP = """
# ChefBotDZ Roadmap
1. Refactorisation & Organisation
2. Sécurité & Robustesse
3. Tests Unitaires
4. Intelligence Augmentée
5. Interface Web
"""

class GPTAgent:
    def __init__(self, role, instructions):
        self.role = role
        self.instructions = instructions
        self.conversation_history = []

    def add_to_history(self, role, content):
        self.conversation_history.append({"role": role, "content": content})

    def send_message(self, message):
        self.add_to_history("user", message)
        messages = [
            {"role": "system", "content": f"{PROJECT_CONTEXT}\n\n{self.instructions}"},
            *self.conversation_history
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=1500,
            )
            content = response.choices[0].message.content.strip()
            self.add_to_history("assistant", content)
            return content
        except Exception as e:
            print(f"Erreur GPT API: {e}")
            return f"Erreur GPT API: {e}"

class ProjectManager:
    def __init__(self):
        self.pilot = GPTAgent(
            role="Pilot",
            instructions="""
            Tu es GPT Pilot. Ton travail:
            - Analyser le code
            - Identifier erreurs et améliorations
            - Proposer du code corrigé
            - Ne jamais discuter de recettes.
            Format de réponse:
            [ANALYSE]
            [PROBLEMES]
            [SOLUTIONS]
            [CODE]
            """
        )
        self.watcher = GPTAgent(
            role="Watcher",
            instructions="""
            Tu es GPT Watcher. Ton travail:
            - Évaluer le code du Pilot
            - Vérifier qualité et conformité
            - Suggérer des améliorations.
            Format de réponse:
            [EVALUATION]
            [FORCES]
            [AMELIORATIONS]
            [CODE_REVISE]
            """
        )

    def get_project_files(self):
        return glob.glob("**/*.py", recursive=True)

    def read_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Erreur de lecture {file_path}: {e}"

    def analyze_project(self):
        files = self.get_project_files()
        if not files:
            print("Aucun fichier Python trouvé.")
            return {}

        first_file = files[0]
        file_content = self.read_file_content(first_file)

        pilot_prompt = f"""
        [FEUILLE_DE_ROUTE]
        {ROADMAP}

        [FICHIER]
        {first_file}

        [CONTENU]
        ```python
        {file_content}
        ```
        """

        pilot_analysis = self.pilot.send_message(pilot_prompt)
        print(f"\n🚀 Analyse Pilot pour {first_file}:")
        print(pilot_analysis)

        watcher_prompt = f"""
        [ANALYSE PILOT]
        {pilot_analysis}
        """

        watcher_review = self.watcher.send_message(watcher_prompt)
        print(f"\n👀 Evaluation Watcher:")
        print(watcher_review)

        results = {
            "file": first_file,
            "pilot_analysis": pilot_analysis,
            "watcher_review": watcher_review
        }

        with open("analysis_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("\n✅ Résultats enregistrés dans analysis_results.json")
        return results

    def analyze_specific_file(self, file_path):
        file_content = self.read_file_content(file_path)

        pilot_prompt = f"""
        [FEUILLE_DE_ROUTE]
        {ROADMAP}

        [FICHIER]
        {file_path}

        [CONTENU]
        ```python
        {file_content}
        ```
        """

        pilot_analysis = self.pilot.send_message(pilot_prompt)

        watcher_prompt = f"""
        [ANALYSE PILOT]
        {pilot_analysis}
        """

        watcher_review = self.watcher.send_message(watcher_prompt)

        return {
            "file": file_path,
            "pilot_analysis": pilot_analysis,
            "watcher_review": watcher_review
        }

if __name__ == "__main__":
    print("\n🔎 Démarrage de l'analyse ChefBotDZ...")
    pm = ProjectManager()
    pm.analyze_project()
