"""
Migration script to add 'model' column to chats table
Run this once: python add_model_column.py
"""
from sqlalchemy import text
from config.db import engine

def add_model_column():
    with engine.connect() as connection:
        try:
            # Add the model column to the chats table
            connection.execute(text(
                "ALTER TABLE chats ADD COLUMN IF NOT EXISTS model VARCHAR"
            ))
            connection.commit()
            print("✅ Successfully added 'model' column to chats table")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_model_column()
