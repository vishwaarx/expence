# 💰 Expense Tracker App

A modern, full-stack expense tracking application built with FastAPI backend and responsive HTML/CSS/JavaScript frontend.

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



## 📚 API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

These provide interactive documentation where you can test API endpoints directly from your browser.
