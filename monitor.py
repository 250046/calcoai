"""
Monitoring script for Calco AI bot
Shows real-time statistics and health checks
"""
from database import db
from datetime import datetime, timedelta
import time

def get_bot_stats():
    """Get bot statistics"""
    try:
        # Total users
        users = db.client.table("users").select("count").execute()
        total_users = len(users.data) if users.data else 0
        
        # Total transactions
        transactions = db.client.table("transactions").select("count").execute()
        total_transactions = len(transactions.data) if transactions.data else 0
        
        # Today's transactions
        today = datetime.now().date()
        today_trans = db.client.table("transactions")\
            .select("*")\
            .gte("date", today.isoformat())\
            .execute()
        today_count = len(today_trans.data) if today_trans.data else 0
        
        # Active loans
        active_loans = db.client.table("loans")\
            .select("count")\
            .eq("status", "pending")\
            .execute()
        loan_count = len(active_loans.data) if active_loans.data else 0
        
        return {
            "total_users": total_users,
            "total_transactions": total_transactions,
            "today_transactions": today_count,
            "active_loans": loan_count,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e)}

def display_stats():
    """Display statistics in console"""
    print("\n" + "="*50)
    print("📊 CALCO AI BOT STATISTICS")
    print("="*50)
    
    stats = get_bot_stats()
    
    if "error" in stats:
        print(f"❌ Error: {stats['error']}")
        return
    
    print(f"\n👥 Total Users: {stats['total_users']}")
    print(f"💰 Total Transactions: {stats['total_transactions']}")
    print(f"📅 Today's Transactions: {stats['today_transactions']}")
    print(f"💸 Active Loans: {stats['active_loans']}")
    print(f"\n🕐 Last Updated: {stats['timestamp']}")
    print("="*50 + "\n")

def monitor_loop(interval: int = 60):
    """Monitor bot in real-time"""
    print("🔍 Starting Calco AI Monitor...")
    print(f"📊 Updating every {interval} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            display_stats()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n👋 Monitor stopped")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "loop":
        # Continuous monitoring
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        monitor_loop(interval)
    else:
        # Single check
        display_stats()
