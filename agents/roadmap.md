# ChefBotDZ - Roadmap Agents GPT-PILOT V1 (2025)

## Objectif
Développer une infrastructure d'agents IA autonomes pour :
- Assister le développement de ChefBotDZ
- Corriger et améliorer le code automatiquement
- Surveiller et analyser les changements
- Orchestrer intelligemment les tâches d'amélioration

## Missions Agents

| Priorité | Mission |
|:---------|:--------|
| 🔥 Critique | Corriger tous les imports cassés |
| 🔥 Critique | Optimiser les prompts de génération de recettes (<400 tokens pour Telegram) |
| ⚡ Important | Vérifier que la réponse GPT respecte la structure : {Nom recette, Ingrédients, Étapes, Calories} |
| ⚡ Important | Optimiser la gestion des erreurs OpenAI et Telegram |
| ⚡ Important | Surveiller tout changement dans `telegram_handler.py`, `main.py`, `openai_services.py` |
| ⚡ Important | Générer un rapport JSON dans `/analysis_results/` après chaque tâche |
| 🌀 Optionnel | Nettoyer les anciens logs inutiles |

## Modes de fonctionnement Orchestrator

| Mode | Description |
|:-----|:------------|
| Standard | Exécution normale de la Roadmap |
| Urgence | Correction prioritaire des bugs critiques |
| Maintenance | Nettoyage et documentation sans modification fonctionnelle |

## Triggers Watcher

- > 30 lignes modifiées = analyse complète
- ≤ 30 lignes modifiées = analyse rapide

## Feedback Loop Automatique

- Après chaque correction → re-scan du fichier corrigé.
- Si nouvelle anomalie détectée → mission automatique générée.

## État actuel (Avril 2025)

| Composant | Status |
|:----------|:-------|
| agent.py | ✅ Basique fonctionnel |
| watcher.py | ✅ Fonctionnel |
| orchestrator.py | ✅ Opérationnel simple |
| run_gpt_pilot.py | ✅ Fonctionne pour tests |
