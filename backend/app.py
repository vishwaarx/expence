from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import json
import os

app = FastAPI(title="Expense Tracker API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class ExpenseCreate(BaseModel):
    description: str = Field(..., min_length=1, description="Expense description")
    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    category: str = Field(default="General", description="Expense category")
    date: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'), description="Expense date")

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    date: str
    created_at: str

class SummaryResponse(BaseModel):
    total_expenses: int
    total_amount: float
    average_amount: float
    category_breakdown: dict

# In-memory storage for expenses (in production, use a database)
EXPENSES_FILE = 'expenses.json'

def load_expenses():
    """Load expenses from JSON file"""
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    """Save expenses to JSON file"""
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

@app.get("/api/expenses", response_model=List[ExpenseResponse])
async def get_expenses():
    """Get all expenses"""
    expenses = load_expenses()
    return expenses

@app.post("/api/expenses", response_model=ExpenseResponse, status_code=201)
async def add_expense(expense: ExpenseCreate):
    """Add a new expense"""
    new_expense = {
        'id': len(load_expenses()) + 1,
        'description': expense.description,
        'amount': expense.amount,
        'category': expense.category,
        'date': expense.date,
        'created_at': datetime.now().isoformat()
    }
    
    expenses = load_expenses()
    expenses.append(new_expense)
    save_expenses(expenses)
    
    return new_expense

@app.delete("/api/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    """Delete an expense by ID"""
    expenses = load_expenses()
    expense = next((e for e in expenses if e['id'] == expense_id), None)
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    expenses = [e for e in expenses if e['id'] != expense_id]
    save_expenses(expenses)
    
    return {"message": "Expense deleted successfully"}

@app.get("/api/expenses/summary", response_model=SummaryResponse)
async def get_summary():
    """Get expense summary statistics"""
    expenses = load_expenses()
    
    if not expenses:
        return SummaryResponse(
            total_expenses=0,
            total_amount=0,
            average_amount=0,
            category_breakdown={}
        )
    
    total_amount = sum(e['amount'] for e in expenses)
    category_breakdown = {}
    
    for expense in expenses:
        category = expense['category']
        if category in category_breakdown:
            category_breakdown[category] += expense['amount']
        else:
            category_breakdown[category] = expense['amount']
    
    return SummaryResponse(
        total_expenses=len(expenses),
        total_amount=total_amount,
        average_amount=total_amount / len(expenses),
        category_breakdown=category_breakdown
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Expense Tracker API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    import socket
    
    def find_available_port(start_port=8080, max_attempts=10):
        """Find an available port starting from start_port"""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return start_port  # Fallback to start_port
    
    port = find_available_port(8080, 20)
    print(f"🚀 Starting FastAPI server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 