import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

class ExpenseDatabase:
    """Simple file-based database for expense storage"""
    
    def __init__(self, file_path: str = 'expenses.json'):
        self.file_path = file_path
    
    def load_expenses(self) -> List[Dict[str, Any]]:
        """Load all expenses from file"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_expenses(self, expenses: List[Dict[str, Any]]) -> None:
        """Save expenses to file"""
        with open(self.file_path, 'w') as f:
            json.dump(expenses, f, indent=2)
    
    def add_expense(self, expense_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new expense"""
        expenses = self.load_expenses()
        
        # Generate new ID
        new_id = max([e.get('id', 0) for e in expenses], default=0) + 1
        
        expense = {
            'id': new_id,
            'description': expense_data['description'],
            'amount': float(expense_data['amount']),
            'category': expense_data.get('category', 'General'),
            'date': expense_data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'created_at': datetime.now().isoformat()
        }
        
        expenses.append(expense)
        self.save_expenses(expenses)
        return expense
    
    def get_expense(self, expense_id: int) -> Optional[Dict[str, Any]]:
        """Get expense by ID"""
        expenses = self.load_expenses()
        return next((e for e in expenses if e['id'] == expense_id), None)
    
    def delete_expense(self, expense_id: int) -> bool:
        """Delete expense by ID"""
        expenses = self.load_expenses()
        original_count = len(expenses)
        
        expenses = [e for e in expenses if e['id'] != expense_id]
        
        if len(expenses) < original_count:
            self.save_expenses(expenses)
            return True
        return False
    
    def update_expense(self, expense_id: int, expense_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update expense by ID"""
        expenses = self.load_expenses()
        
        for i, expense in enumerate(expenses):
            if expense['id'] == expense_id:
                expenses[i].update({
                    'description': expense_data.get('description', expense['description']),
                    'amount': float(expense_data.get('amount', expense['amount'])),
                    'category': expense_data.get('category', expense['category']),
                    'date': expense_data.get('date', expense['date'])
                })
                self.save_expenses(expenses)
                return expenses[i]
        
        return None
    
    def get_expenses_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get expenses filtered by category"""
        expenses = self.load_expenses()
        return [e for e in expenses if e['category'] == category]
    
    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get expenses within date range"""
        expenses = self.load_expenses()
        return [e for e in expenses if start_date <= e['date'] <= end_date]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get expense summary statistics"""
        expenses = self.load_expenses()
        
        if not expenses:
            return {
                'total_expenses': 0,
                'total_amount': 0,
                'average_amount': 0,
                'category_breakdown': {}
            }
        
        total_amount = sum(e['amount'] for e in expenses)
        category_breakdown = {}
        
        for expense in expenses:
            category = expense['category']
            if category in category_breakdown:
                category_breakdown[category] += expense['amount']
            else:
                category_breakdown[category] = expense['amount']
        
        return {
            'total_expenses': len(expenses),
            'total_amount': total_amount,
            'average_amount': round(total_amount / len(expenses), 2),
            'category_breakdown': category_breakdown
        } 