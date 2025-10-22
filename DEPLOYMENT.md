# Deployment Guide

## Production Deployment Options

### Option 1: Static Hosting (Frontend) + Cloud API (Backend)

#### Frontend Deployment (Vercel/Netlify)

**Vercel (Recommended for Astro):**
```bash
cd frontend
npm run build

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

**Netlify:**
```bash
cd frontend
npm run build

# Deploy dist/ folder
netlify deploy --prod --dir=dist
```

**Configuration:**
- Build command: `npm run build`
- Output directory: `dist`
- Node version: 18+

**Environment Variables:**
- `PUBLIC_API_URL`: Your backend API URL

#### Backend Deployment (Cloud Provider)

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

**AWS Lambda + API Gateway:**
- Use Mangum adapter for FastAPI
- Package with dependencies
- Deploy via SAM or CDK

**Google Cloud Run:**
```bash
# Create Dockerfile
gcloud run deploy flight-delay-api \
  --source . \
  --platform managed \
  --region us-central1
```

### Option 2: Docker Container (Full Stack)

**Create Dockerfile:**
```dockerfile
# Multi-stage build
FROM python:3.11-slim as backend

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY models ./models

FROM node:18 as frontend-builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build

FROM python:3.11-slim

WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend-builder /app/dist /app/frontend/dist

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 4321

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and Run:**
```bash
docker build -t flight-delay-app .
docker run -p 8000:8000 flight-delay-app
```

### Option 3: Traditional Server (VPS)

**Setup on Ubuntu/Debian:**

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nodejs npm nginx

# Clone repository
git clone <your-repo>
cd flight-delay-hackathon-wso-template

# Setup Python
python3 -m venv flight_model_env
source flight_model_env/bin/activate
pip install -r requirements.txt

# Setup Node.js
cd frontend
npm install
npm run build

# Configure nginx
sudo nano /etc/nginx/sites-available/flight-delay
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Start Services with systemd:**

Backend service (`/etc/systemd/system/flight-delay-api.service`):
```ini
[Unit]
Description=Flight Delay API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/flight-delay-hackathon-wso-template
Environment="PATH=/path/to/flight_model_env/bin"
ExecStart=/path/to/flight_model_env/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable flight-delay-api
sudo systemctl start flight-delay-api
```

## Environment Configuration

### Backend Environment Variables

Create `.env` file in `backend/`:
```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=../models

# CORS Origins (production URLs)
CORS_ORIGINS=["https://yourdomain.com"]

# Logging
LOG_LEVEL=INFO
```

### Frontend Environment Variables

Create `.env` file in `frontend/`:
```bash
# API URL
PUBLIC_API_URL=https://api.yourdomain.com
```

## Pre-Deployment Checklist

### Backend
- [ ] Model files are included
- [ ] Dependencies are up to date
- [ ] CORS configured for production domain
- [ ] API keys/secrets in environment variables
- [ ] Error logging configured
- [ ] Health check endpoint tested
- [ ] Rate limiting configured (if needed)

### Frontend
- [ ] API URL updated to production
- [ ] Build tested locally (`npm run build && npm run preview`)
- [ ] All pages accessible
- [ ] Mobile responsive verified
- [ ] Assets optimized
- [ ] Error boundaries in place

## Security Considerations

### Backend
1. **API Security:**
   - Add authentication (JWT, OAuth)
   - Implement rate limiting
   - Use HTTPS only
   - Validate all inputs
   - Add API keys for sensitive endpoints

2. **CORS Configuration:**
   ```python
   # Update backend/main.py
   origins = [
       "https://yourdomain.com",
       "https://www.yourdomain.com",
   ]
   ```

3. **Environment Variables:**
   - Never commit secrets
   - Use environment variables for configuration
   - Use secret management services in production

### Frontend
1. **Security Headers:**
   - Set in hosting provider or nginx
   - CSP, X-Frame-Options, etc.

2. **API Keys:**
   - Never expose backend API keys in frontend
   - Use environment variables properly

## Monitoring and Logging

### Backend Monitoring
```python
# Add to backend/main.py
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
```

### Frontend Monitoring
- Use analytics (Google Analytics, Plausible)
- Error tracking (Sentry)
- Performance monitoring (Web Vitals)

## Backup Strategy

### Model Files
```bash
# Backup models directory
tar -czf models-backup-$(date +%Y%m%d).tar.gz models/
```

### Database (if added later)
- Regular database backups
- Automated backup scripts
- Off-site backup storage

## Performance Optimization

### Backend
1. **Caching:**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def get_airports():
       # Cache airport list
   ```

2. **Async operations** - Already implemented with FastAPI

3. **Model optimization:**
   - Use model quantization
   - Consider model serving solutions (TensorFlow Serving, TorchServe)

### Frontend
1. **Already Optimized:**
   - Astro SSR for fast initial loads
   - Static asset optimization
   - Minimal JavaScript

2. **CDN:**
   - Serve static assets via CDN
   - Cache-Control headers

## Testing in Production

### Smoke Tests
```bash
# Test backend health
curl https://api.yourdomain.com/health

# Test prediction endpoint
curl -X POST https://api.yourdomain.com/predict \
  -H "Content-Type: application/json" \
  -d '{"day_of_week": 5, "origin_airport_id": 13930, "dest_airport_id": 12892}'

# Test frontend
curl https://yourdomain.com
```

### Load Testing
```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test API
ab -n 1000 -c 10 http://localhost:8000/health
```

## Rollback Plan

1. Keep previous deployment artifacts
2. Use git tags for versions
3. Database migration rollback scripts
4. Quick rollback procedure documented

## Cost Estimation

### Free Tier Options
- **Frontend:** Vercel/Netlify (free tier available)
- **Backend:** 
  - Heroku Free Dynos (limited)
  - Railway (free tier)
  - Render (free tier)

### Paid Options
- **VPS:** DigitalOcean ($5-10/month)
- **Managed:** Heroku ($7-25/month)
- **Serverless:** AWS Lambda (pay per request)

## Maintenance

### Regular Tasks
- [ ] Update dependencies monthly
- [ ] Review logs weekly
- [ ] Monitor performance metrics
- [ ] Retrain model with new data
- [ ] Security patches
- [ ] Backup verification

---

Choose the deployment option that best fits your needs and infrastructure!
