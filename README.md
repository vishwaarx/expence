# 💰 Expense Tracker App

A modern, full-stack expense tracking application built with FastAPI backend and responsive HTML/CSS/JavaScript frontend.

## 🚀 Features

- **Add Expenses**: Track expenses with description, amount, category, and date
- **View History**: See all your expenses in a beautiful, organized list
- **Delete Expenses**: Remove unwanted entries with confirmation
- **Summary Statistics**: Real-time overview of total expenses, amounts, and averages
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Interactive API Documentation**: Built-in Swagger UI for API exploration

## 📁 Project Structure

```
expense-tracker/
├── backend/
│   ├── app.py          # Main FastAPI application
│   ├── models.py       # Data models and classes
│   └── database.py     # Database utilities
├── frontend/
│   └── index.html      # Responsive web interface
├── requirements.txt     # Python dependencies
└── README.md          # This file
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd expense-tracker
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI backend**
   ```bash
   python run.py
   ```
   The server will start at `http://localhost:8080`
   API documentation will be available at `http://localhost:8080/docs`

4. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or serve it using a local server (recommended)

### Running with a Local Server (Optional)

For better development experience, you can serve the frontend using Python's built-in server:

```bash
# In a new terminal, from the project root
python -m http.server 8000
```

Then open `http://localhost:8000/frontend/index.html` in your browser.

## 🎯 API Endpoints

### GET `/api/expenses`
Returns all expenses in JSON format.

**Response:**
```json
[
  {
    "id": 1,
    "description": "Groceries",
    "amount": 45.50,
    "category": "Food",
    "date": "2024-01-15",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### POST `/api/expenses`
Add a new expense.

**Request Body:**
```json
{
  "description": "Gas",
  "amount": 35.00,
  "category": "Transportation",
  "date": "2024-01-15"
}
```

### DELETE `/api/expenses/{id}`
Delete an expense by ID.

### GET `/api/expenses/summary`
Get expense summary statistics.

**Response:**
```json
{
  "total_expenses": 5,
  "total_amount": 150.75,
  "average_amount": 30.15,
  "category_breakdown": {
    "Food": 45.50,
    "Transportation": 35.00
  }
}
```

## 📚 API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

These provide interactive documentation where you can test API endpoints directly from your browser.

## 🎨 Frontend Features

- **Modern Design**: Gradient backgrounds and smooth animations
- **Responsive Layout**: Adapts to different screen sizes
- **Real-time Updates**: Automatic refresh after adding/deleting expenses
- **Form Validation**: Client-side validation for better UX
- **Success/Error Messages**: Clear feedback for user actions
- **Category Badges**: Visual category indicators
- **Summary Cards**: Quick overview of expense statistics

## 🔧 Customization

### Adding New Categories
Edit the category dropdown in `frontend/index.html`:

```html
<select id="category" name="category">
    <option value="General">General</option>
    <option value="Food">Food</option>
    <option value="Transportation">Transportation</option>
    <!-- Add your custom categories here -->
    <option value="Custom Category">Custom Category</option>
</select>
```

### Changing Colors
Modify the CSS variables in the `<style>` section of `frontend/index.html`:

```css
/* Primary gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Accent colors */
.btn-danger {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
}
```

## 🧪 Testing

### Manual Testing
1. Start the backend server with `python run.py`
2. Open the frontend in your browser
3. Add some test expenses
4. Verify the summary statistics update
5. Test deleting expenses
6. Check responsive design on different screen sizes

### API Testing with curl

```bash
# Get all expenses
curl http://localhost:8080/api/expenses

# Add a new expense
curl -X POST http://localhost:8080/api/expenses \
  -H "Content-Type: application/json" \
  -d '{"description":"Test Expense","amount":25.50,"category":"General"}'

# Get summary
curl http://localhost:8080/api/expenses/summary
```

### Automated Testing
Run the test suite:

```bash
# Run the main test script
python test_app.py

# Run unit tests
cd backend
python -m pytest tests.py -v
```

## 🚀 Deployment

### Backend Deployment
- Deploy to platforms like Heroku, Railway, or DigitalOcean
- Set environment variables for production settings
- Use a proper database (PostgreSQL, MySQL) instead of JSON file
- FastAPI works great with ASGI servers like Uvicorn

### Frontend Deployment
- Deploy to GitHub Pages, Netlify, or Vercel
- Update the API_BASE_URL in the JavaScript to point to your deployed backend

## 🔒 Security Considerations

- Input validation on both frontend and backend (FastAPI provides automatic validation)
- CORS configuration for cross-origin requests
- Consider adding authentication for multi-user support
- Use HTTPS in production
- Implement rate limiting for API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if port 8080 is already in use
- Verify Python and FastAPI are installed correctly
- Check the console for error messages

**Frontend can't connect to backend:**
- Ensure the FastAPI server is running on `http://localhost:3000`
- Check browser console for CORS errors
- Verify the API_BASE_URL in the JavaScript code

**Expenses not saving:**
- Check file permissions for the `expenses.json` file
- Verify the backend has write access to the directory

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Review the console logs for error messages
3. Ensure all dependencies are installed correctly
4. Verify the server is running and accessible
5. Check the interactive API documentation at `http://localhost:3000/docs` 