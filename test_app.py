#!/usr/bin/env python3
"""
Test script for Expense Tracker
Run this to test the API endpoints
"""

import requests
import json
import time
import sys

API_BASE_URL = "http://localhost:8080/api"

def test_api_connection():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/expenses", timeout=5)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def test_add_expense():
    """Test adding an expense"""
    expense_data = {
        "description": "Test Groceries",
        "amount": 45.50,
        "category": "Food",
        "date": "2024-01-15"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/expenses",
            json=expense_data,
            timeout=5
        )
        
        if response.status_code == 201:
            print("✅ Add expense test passed")
            return response.json()
        else:
            print(f"❌ Add expense test failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Add expense test error: {e}")
        return None

def test_get_expenses():
    """Test getting all expenses"""
    try:
        response = requests.get(f"{API_BASE_URL}/expenses", timeout=5)
        
        if response.status_code == 200:
            expenses = response.json()
            print(f"✅ Get expenses test passed - Found {len(expenses)} expenses")
            return expenses
        else:
            print(f"❌ Get expenses test failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Get expenses test error: {e}")
        return []

def test_get_summary():
    """Test getting expense summary"""
    try:
        response = requests.get(f"{API_BASE_URL}/expenses/summary", timeout=5)
        
        if response.status_code == 200:
            summary = response.json()
            print("✅ Get summary test passed")
            print(f"   Total expenses: {summary['total_expenses']}")
            print(f"   Total amount: ${summary['total_amount']:.2f}")
            print(f"   Average amount: ${summary['average_amount']:.2f}")
            return summary
        else:
            print(f"❌ Get summary test failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Get summary test error: {e}")
        return None

def test_delete_expense(expense_id):
    """Test deleting an expense"""
    try:
        response = requests.delete(f"{API_BASE_URL}/expenses/{expense_id}", timeout=5)
        
        if response.status_code == 200:
            print("✅ Delete expense test passed")
            return True
        else:
            print(f"❌ Delete expense test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Delete expense test error: {e}")
        return False

def run_tests():
    """Run all tests"""
    print("🧪 Testing Expense Tracker API")
    print("=" * 40)
    
    # Test 1: Check if API is running
    print("\n1. Testing API connection...")
    if not test_api_connection():
        print("❌ API is not running. Please start the server first:")
        print("   python run.py")
        return False
    print("✅ API is running")
    
    # Test 2: Add an expense
    print("\n2. Testing add expense...")
    added_expense = test_add_expense()
    if not added_expense:
        return False
    
    # Test 3: Get all expenses
    print("\n3. Testing get expenses...")
    expenses = test_get_expenses()
    if not expenses:
        return False
    
    # Test 4: Get summary
    print("\n4. Testing get summary...")
    summary = test_get_summary()
    if not summary:
        return False
    
    # Test 5: Delete the test expense
    print("\n5. Testing delete expense...")
    if added_expense and 'id' in added_expense:
        test_delete_expense(added_expense['id'])
    
    print("\n🎉 All tests completed!")
    return True

def main():
    """Main function"""
    try:
        success = run_tests()
        if success:
            print("\n✅ All tests passed! Your Expense Tracker is working correctly.")
            print("\n💡 Next steps:")
            print("   - Open frontend/index.html in your browser")
            print("   - Start adding your real expenses!")
        else:
            print("\n❌ Some tests failed. Please check the server and try again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 