import unittest
import json
import os
import tempfile
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app, load_expenses, save_expenses

class ExpenseTrackerTestCase(unittest.TestCase):
    """Test cases for the Expense Tracker API"""
    
    def setUp(self):
        """Set up test environment"""
        from fastapi.testclient import TestClient
        self.client = TestClient(app)
        
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        # Patch the expenses file path
        self.patcher = patch('app.EXPENSES_FILE', self.temp_file.name)
        self.patcher.start()
        
        # Initialize with empty expenses
        save_expenses([])
    
    def tearDown(self):
        """Clean up after tests"""
        self.patcher.stop()
        os.unlink(self.temp_file.name)
    
    def test_get_expenses_empty(self):
        """Test getting expenses when none exist"""
        response = self.client.get('/api/expenses')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    
    def test_add_expense_valid(self):
        """Test adding a valid expense"""
        expense_data = {
            'description': 'Test Expense',
            'amount': 25.50,
            'category': 'General',
            'date': '2024-01-15'
        }
        
        response = self.client.post('/api/expenses', json=expense_data)
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['description'], 'Test Expense')
        self.assertEqual(data['amount'], 25.50)
        self.assertEqual(data['category'], 'General')
        self.assertEqual(data['date'], '2024-01-15')
    
    def test_add_expense_missing_fields(self):
        """Test adding expense with missing required fields"""
        expense_data = {'description': 'Test Expense'}  # Missing amount
        
        response = self.client.post('/api/expenses', json=expense_data)
        
        self.assertEqual(response.status_code, 422)  # FastAPI validation error
    
    def test_add_expense_invalid_amount(self):
        """Test adding expense with invalid amount"""
        expense_data = {
            'description': 'Test Expense',
            'amount': 'invalid'
        }
        
        response = self.client.post('/api/expenses', json=expense_data)
        
        self.assertEqual(response.status_code, 422)  # FastAPI validation error
    
    def test_add_expense_negative_amount(self):
        """Test adding expense with negative amount"""
        expense_data = {
            'description': 'Test Expense',
            'amount': -10.00
        }
        
        response = self.client.post('/api/expenses', json=expense_data)
        
        self.assertEqual(response.status_code, 422)  # FastAPI validation error
    
    def test_delete_expense(self):
        """Test deleting an expense"""
        # First add an expense
        expense_data = {
            'description': 'Test Expense',
            'amount': 25.50,
            'category': 'General'
        }
        
        add_response = self.client.post('/api/expenses', json=expense_data)
        added_expense = add_response.json()
        
        # Then delete it
        delete_response = self.client.delete(f'/api/expenses/{added_expense["id"]}')
        self.assertEqual(delete_response.status_code, 200)
        
        # Verify it's deleted
        get_response = self.client.get('/api/expenses')
        expenses = get_response.json()
        self.assertEqual(len(expenses), 0)
    
    def test_delete_nonexistent_expense(self):
        """Test deleting an expense that doesn't exist"""
        response = self.client.delete('/api/expenses/999')
        self.assertEqual(response.status_code, 404)
    
    def test_get_summary_empty(self):
        """Test getting summary with no expenses"""
        response = self.client.get('/api/expenses/summary')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_expenses'], 0)
        self.assertEqual(data['total_amount'], 0)
        self.assertEqual(data['average_amount'], 0)
        self.assertEqual(data['category_breakdown'], {})
    
    def test_get_summary_with_expenses(self):
        """Test getting summary with expenses"""
        # Add some expenses
        expenses = [
            {'description': 'Food', 'amount': 25.00, 'category': 'Food'},
            {'description': 'Gas', 'amount': 35.00, 'category': 'Transportation'},
            {'description': 'Movie', 'amount': 15.00, 'category': 'Entertainment'}
        ]
        
        for expense in expenses:
            self.client.post('/api/expenses', json=expense)
        
        response = self.client.get('/api/expenses/summary')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['total_expenses'], 3)
        self.assertEqual(data['total_amount'], 75.00)
        self.assertEqual(data['average_amount'], 25.00)
        self.assertIn('Food', data['category_breakdown'])
        self.assertIn('Transportation', data['category_breakdown'])
        self.assertIn('Entertainment', data['category_breakdown'])

if __name__ == '__main__':
    unittest.main() 