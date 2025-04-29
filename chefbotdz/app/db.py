# app/db.py

"""
Module de gestion de la base de données pour ChefBotDZ.
Utilise SQLite pour l'instant, prévu pour migration facile vers PostgreSQL.
"""

import sqlite3
import os

# Chemin de la base de données locale
DB_PATH = os.getenv("DB_PATH", "db.sqlite3")

# Connexion SQLite
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # pour récupérer les résultats sous forme de dictionnaire
    return conn

# Initialisation de la base de données
def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Création table utilisateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE,
        is_premium BOOLEAN DEFAULT 0,
        recipes_today INTEGER DEFAULT 0,
        last_access_date TEXT
    )
    """)

    # Création table pending_recipes pour choix multiple
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pending_recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT,
        recipes TEXT,  -- Liste de recettes JSON encodée
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Création table paiements
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT,
        transaction_code TEXT,
        payment_method TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Fonctions de gestion des utilisateurs
def add_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO users (telegram_id)
    VALUES (?)
    """, (telegram_id,))
    conn.commit()
    conn.close()

def update_user_premium(telegram_id, is_premium=True):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users
    SET is_premium = ?, recipes_today = 0
    WHERE telegram_id = ?
    """, (int(is_premium), telegram_id))
    conn.commit()
    conn.close()

def increment_user_recipe_count(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users
    SET recipes_today = recipes_today + 1
    WHERE telegram_id = ?
    """, (telegram_id,))
    conn.commit()
    conn.close()

def reset_daily_counters():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users
    SET recipes_today = 0
    """)
    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users
    WHERE telegram_id = ?
    """, (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Fonctions de gestion des choix multiples de recettes
def save_pending_recipes(telegram_id, recipes_json):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO pending_recipes (telegram_id, recipes)
    VALUES (?, ?)
    """, (telegram_id, recipes_json))
    conn.commit()
    conn.close()

def get_pending_recipes(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM pending_recipes
    WHERE telegram_id = ?
    ORDER BY created_at DESC
    LIMIT 1
    """, (telegram_id,))
    pending = cursor.fetchone()
    conn.close()
    return pending

def delete_pending_recipes(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM pending_recipes
    WHERE telegram_id = ?
    """, (telegram_id,))
    conn.commit()
    conn.close()

# Fonctions paiements
def save_payment(telegram_id, transaction_code, payment_method):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO payments (telegram_id, transaction_code, payment_method)
    VALUES (?, ?, ?)
    """, (telegram_id, transaction_code, payment_method))
    conn.commit()
    conn.close()

def validate_payment(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE payments
    SET status = 'validated'
    WHERE telegram_id = ? AND status = 'pending'
    """, (telegram_id,))
    conn.commit()
    conn.close()
