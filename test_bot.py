"""
Test script to verify bot components
"""
import asyncio
from database import db
from ai_parser import ai_parser
from config import BOT_TOKEN, OPENAI_API_KEY, SUPABASE_URL

def test_config():
    print("🔍 Testing configuration...")
    assert BOT_TOKEN, "❌ BOT_TOKEN not set"
    assert OPENAI_API_KEY, "❌ OPENAI_API_KEY not set"
    assert SUPABASE_URL, "❌ SUPABASE_URL not set"
    print("✅ Configuration OK")

def test_database():
    print("\n🔍 Testing database connection...")
    try:
        # Try to query users table
        result = db.client.table("users").select("count").execute()
        print("✅ Database connection OK")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    return True

def test_ai_parser():
    print("\n🔍 Testing AI parser...")
    try:
        # Test transaction parsing
        result = ai_parser.parse_transaction("I spent 15000 on food", "uz")
        if result and "amount" in result:
            print(f"✅ AI parser OK - Parsed: {result}")
        else:
            print("⚠️  AI parser returned no result (might be API issue)")
    except Exception as e:
        print(f"❌ AI parser error: {e}")

def main():
    print("🧪 Running Calco AI Tests\n")
    print("=" * 50)
    
    test_config()
    
    if test_database():
        print("\n✅ Database is ready!")
    else:
        print("\n⚠️  Please run schema.sql in Supabase first")
        print(f"   Go to: {SUPABASE_URL}/project/_/sql")
    
    test_ai_parser()
    
    print("\n" + "=" * 50)
    print("🎉 Tests complete! You can now run: python bot.py")

if __name__ == "__main__":
    main()
