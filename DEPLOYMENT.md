# 🚀 Deployment Guide

This guide covers different deployment options for the Expense Tracker application.

## 📋 Prerequisites

- Python 3.7 or higher
- Git (for version control)
- A web server or hosting platform

## 🏠 Local Development

### Quick Start
```bash
# Clone or download the project
cd expense-tracker

# Install dependencies
pip install -r requirements.txt

# Start the server
python run.py

# Open in browser
# http://localhost:5000 (API)
# frontend/index.html (UI)
```

### Testing
```bash
# Run the test suite
python test_app.py

# Run unit tests
cd backend
python -m unittest tests.py
```

## ☁️ Cloud Deployment Options

### 1. Heroku Deployment

#### Setup
```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create your-expense-tracker

# Add Python buildpack
heroku buildpacks:set heroku/python
```

#### Create `Procfile`
```bash
# Create Procfile in project root
echo "web: cd backend && python app.py" > Procfile
```

#### Deploy
```bash
# Add all files
git add .

# Commit changes
git commit -m "Initial deployment"

# Push to Heroku
git push heroku main

# Open the app
heroku open
```

### 2. Railway Deployment

#### Setup
1. Go to [Railway](https://railway.app)
2. Connect your GitHub repository
3. Set environment variables:
   - `PORT`: 5000
   - `FLASK_ENV`: production

#### Deploy
```bash
# Railway will automatically deploy from your Git repository
# No additional configuration needed
```

### 3. DigitalOcean App Platform

#### Setup
1. Go to [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
2. Connect your GitHub repository
3. Configure the app:
   - **Source Directory**: `/`
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `cd backend && python app.py`
   - **Port**: 5000

### 4. Vercel Deployment (Frontend Only)

#### Setup
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
vercel frontend/

# Update API_BASE_URL in frontend files to point to your backend
```

## 🗄️ Database Options

### Current: JSON File Storage
- **Pros**: Simple, no setup required
- **Cons**: Not suitable for production, no concurrent access
- **Use Case**: Development, small personal projects

### Production: PostgreSQL
```python
# Install additional requirements
pip install psycopg2-binary

# Update database.py to use PostgreSQL
import psycopg2
from psycopg2.extras import RealDictCursor

class ExpenseDatabase:
    def __init__(self, database_url):
        self.database_url = database_url
    
    def get_connection(self):
        return psycopg2.connect(self.database_url)
    
    def load_expenses(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM expenses ORDER BY created_at DESC")
                return [dict(row) for row in cur.fetchall()]
    
    def add_expense(self, expense_data):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO expenses (description, amount, category, date, created_at)
                    VALUES (%s, %s, %s, %s, %s) RETURNING *
                """, (
                    expense_data['description'],
                    expense_data['amount'],
                    expense_data.get('category', 'General'),
                    expense_data.get('date'),
                    datetime.now().isoformat()
                ))
                return dict(cur.fetchone())
```

### Database Schema
```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(100) DEFAULT 'General',
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_expenses_date ON expenses(date);
CREATE INDEX idx_expenses_category ON expenses(category);
```

## 🔒 Security Considerations

### Environment Variables
```bash
# Create .env file
FLASK_SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/db
CORS_ORIGINS=https://yourdomain.com
```

### Update app.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

# Configure CORS for production
CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))
```

### HTTPS Setup
```python
# For production, use HTTPS
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        ssl_context='adhoc'  # Requires: pip install pyOpenSSL
    )
```

## 📊 Monitoring & Logging

### Add Logging
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/expense_tracker.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Expense Tracker startup')
```

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })
```

## 🔧 Performance Optimization

### Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/expenses/summary')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_summary():
    # ... existing code
```

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/expenses', methods=['POST'])
@limiter.limit("10 per minute")
def add_expense():
    # ... existing code
```

## 📱 Mobile Deployment

### Progressive Web App (PWA)
Add to `frontend/index.html`:
```html
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#667eea">
```

Create `frontend/manifest.json`:
```json
{
  "name": "Expense Tracker",
  "short_name": "Expenses",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#667eea",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

## 🧪 Testing in Production

### Load Testing
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test API endpoints
ab -n 1000 -c 10 http://your-app.herokuapp.com/api/expenses
```

### Monitoring
```python
# Add performance monitoring
import time

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if hasattr(g, 'start'):
        diff = time.time() - g.start
        app.logger.info(f'{request.method} {request.path} - {response.status_code} - {diff:.3f}s')
    return response
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   # Kill the process
   kill -9 <PID>
   ```

2. **CORS errors**
   - Check CORS configuration in app.py
   - Verify frontend URL is in allowed origins

3. **Database connection issues**
   - Verify DATABASE_URL environment variable
   - Check database credentials and permissions

4. **Static files not loading**
   - Ensure proper file paths
   - Check web server configuration

### Debug Mode
```python
# Enable debug mode for development
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Implement session management
- Use shared database

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching strategies

### Microservices Architecture
- Split into separate services
- Use message queues (Redis, RabbitMQ)
- Implement API gateway

## 📞 Support

For deployment issues:
1. Check the logs: `heroku logs --tail`
2. Verify environment variables
3. Test locally first
4. Check platform-specific documentation 