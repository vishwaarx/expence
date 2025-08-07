from datetime import datetime
from typing import Optional, Dict, Any

class Expense:
    """Data model for expense entries"""
    
    def __init__(self, description: str, amount: float, category: str = "General", 
                 date: Optional[str] = None, expense_id: Optional[int] = None):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        self.id = expense_id
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert expense to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Expense':
        """Create expense from dictionary"""
        return cls(
            description=data['description'],
            amount=data['amount'],
            category=data.get('category', 'General'),
            date=data.get('date'),
            expense_id=data.get('id')
        )
    
    def validate(self) -> bool:
        """Validate expense data"""
        if not self.description or not self.description.strip():
            return False
        if self.amount <= 0:
            return False
        return True

class ExpenseSummary:
    """Data model for expense summary statistics"""
    
    def __init__(self, total_expenses: int = 0, total_amount: float = 0, 
                 average_amount: float = 0, category_breakdown: Dict[str, float] = None):
        self.total_expenses = total_expenses
        self.total_amount = total_amount
        self.average_amount = average_amount
        self.category_breakdown = category_breakdown or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary for JSON serialization"""
        return {
            'total_expenses': self.total_expenses,
            'total_amount': self.total_amount,
            'average_amount': round(self.average_amount, 2),
            'category_breakdown': self.category_breakdown
        }
    
    @classmethod
    def from_expenses(cls, expenses: list) -> 'ExpenseSummary':
        """Create summary from list of expenses"""
        if not expenses:
            return cls()
        
        total_amount = sum(expense['amount'] for expense in expenses)
        category_breakdown = {}
        
        for expense in expenses:
            category = expense['category']
            if category in category_breakdown:
                category_breakdown[category] += expense['amount']
            else:
                category_breakdown[category] = expense['amount']
        
        return cls(
            total_expenses=len(expenses),
            total_amount=total_amount,
            average_amount=total_amount / len(expenses),
            category_breakdown=category_breakdown
        ) 