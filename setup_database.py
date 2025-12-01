"""
Setup script to create database tables in Supabase
Run this once before starting the bot
"""
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

def setup_database():
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("🔧 Setting up database tables...")
    
    # Read schema file
    with open("schema.sql", "r") as f:
        schema = f.read()
    
    # Execute schema (note: Supabase client doesn't directly support SQL execution)
    # You need to run schema.sql manually in Supabase SQL Editor
    
    print("✅ Please run the SQL from schema.sql in your Supabase SQL Editor")
    print(f"   Go to: {SUPABASE_URL}/project/_/sql")
    print("\n📋 Copy and paste the contents of schema.sql")
    
    # Test connection
    try:
        result = client.table("users").select("count").execute()
        print("\n✅ Database connection successful!")
    except Exception as e:
        print(f"\n❌ Database connection failed: {e}")
        print("   Make sure you've run the schema.sql in Supabase first")

if __name__ == "__main__":
    setup_database()
