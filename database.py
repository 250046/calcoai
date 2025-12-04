from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime, date
from typing import Optional, List, Dict

class Database:
    def __init__(self):
        try:
            self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"Database connection error: {e}")
            raise
    
    # User operations
    def get_user(self, telegram_id: int) -> Optional[Dict]:
        response = self.client.table("users").select("*").eq("telegram_id", telegram_id).execute()
        return response.data[0] if response.data else None
    
    def create_user(self, telegram_id: int, name: str, language: str = "uz", currency: str = "UZS") -> Dict:
        data = {
            "telegram_id": telegram_id,
            "name": name,
            "language": language,
            "currency": currency,
            "created_at": datetime.now().isoformat()
        }
        response = self.client.table("users").insert(data).execute()
        return response.data[0]
    
    def update_user_language(self, telegram_id: int, language: str):
        self.client.table("users").update({"language": language}).eq("telegram_id", telegram_id).execute()
    
    def update_user_currency(self, telegram_id: int, currency: str):
        self.client.table("users").update({"currency": currency}).eq("telegram_id", telegram_id).execute()
    
    # Transaction operations
    def add_transaction(self, user_id: int, amount: float, trans_type: str, 
                       category: str, description: str, trans_date: Optional[date] = None) -> Dict:
        data = {
            "user_id": user_id,
            "amount": amount,
            "type": trans_type,
            "category": category,
            "description": description,
            "date": (trans_date or date.today()).isoformat()
        }
        response = self.client.table("transactions").insert(data).execute()
        return response.data[0]
    
    def get_transactions(self, user_id: int, limit: int = 10) -> List[Dict]:
        response = self.client.table("transactions")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("date", desc=True)\
            .order("id", desc=True)\
            .limit(limit)\
            .execute()
        return response.data
    
    def get_monthly_summary(self, user_id: int, year: int, month: int) -> Dict:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        response = self.client.table("transactions")\
            .select("*")\
            .eq("user_id", user_id)\
            .gte("date", start_date.isoformat())\
            .lt("date", end_date.isoformat())\
            .execute()
        
        transactions = response.data
        income = sum(t["amount"] for t in transactions if t["type"] == "income")
        expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        
        return {
            "income": income,
            "expense": expense,
            "balance": income - expense,
            "transactions": transactions
        }
    
    # Loan operations
    def add_loan(self, user_id: int, person_name: str, amount: float, 
                 return_date: Optional[date] = None) -> Dict:
        data = {
            "user_id": user_id,
            "person_name": person_name,
            "amount": amount,
            "given_date": date.today().isoformat(),
            "return_date": return_date.isoformat() if return_date else None,
            "status": "pending"
        }
        response = self.client.table("loans").insert(data).execute()
        return response.data[0]
    
    def get_loans(self, user_id: int, status: Optional[str] = None) -> List[Dict]:
        query = self.client.table("loans").select("*").eq("user_id", user_id)
        if status:
            query = query.eq("status", status)
        response = query.order("given_date", desc=True).execute()
        return response.data
    
    def mark_loan_paid(self, loan_id: int):
        self.client.table("loans").update({"status": "paid"}).eq("id", loan_id).execute()

db = Database()
