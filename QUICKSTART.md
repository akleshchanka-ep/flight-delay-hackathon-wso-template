# Flight Delay Predictor - Quick Reference

## 🚀 Start the Application

### One Command (Full Stack)
```bash
./run_fullstack.sh
```

### Separate Commands
```bash
# Terminal 1 - Backend
cd backend && source ../flight_model_env/bin/activate && uvicorn main:app --reload

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

## 🌐 URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:4321 | Web UI |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |

## 📱 Pages

| Page | URL | Purpose |
|------|-----|---------|
| Home | / | Landing page with navigation |
| Quick Predict | /predict | Simple prediction interface |
| Custom Predict | /custom | Advanced features + batch mode |

## 🔌 API Endpoints

### GET /airports
Retrieve list of airports

**Query Parameters:**
- `limit` (optional): Max results (default: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "total": 70,
  "airports": [
    {
      "airport_id": 10397,
      "airport_name": "Hartsfield-Jackson Atlanta International",
      "city": "Atlanta",
      "state": "GA"
    }
  ]
}
```

### POST /predict
Get flight delay prediction

**Request Body:**
```json
{
  "day_of_week": 5,
  "origin_airport_id": 13930,
  "dest_airport_id": 12892
}
```

**Response:**
```json
{
  "delay_probability": 0.3245,
  "confidence": 0.8912,
  "prediction": "LIKELY ON TIME"
}
```

## 🎯 Common Tasks

### Test API with curl
```bash
# Get airports
curl http://localhost:8000/airports?limit=10

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"day_of_week": 5, "origin_airport_id": 13930, "dest_airport_id": 12892}'
```

### Build Frontend for Production
```bash
cd frontend
npm run build
npm run preview
```

### Run Tests
```bash
# Backend tests
cd backend
python test_api.py

# Example client
python ../example_client.py
```

## 🛠 Troubleshooting

### Backend won't start
```bash
# Activate virtual environment
source flight_model_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 4321 (frontend)
lsof -ti:4321 | xargs kill -9
```

## 📊 Day of Week Values

| Day | Value |
|-----|-------|
| Monday | 1 |
| Tuesday | 2 |
| Wednesday | 3 |
| Thursday | 4 |
| Friday | 5 |
| Saturday | 6 |
| Sunday | 7 |

## 🎨 Features

### Quick Predict
- ✅ Dropdown day selection
- ✅ Airport dropdowns (auto-loaded)
- ✅ Instant results
- ✅ Visual indicators

### Custom Predict
- ✅ Radio button day selection
- ✅ Airport search
- ✅ Multi-select lists
- ✅ Batch mode (predict entire week)
- ✅ Comparison table
- ✅ Best/worst day analysis

## 📁 Project Structure

```
.
├── backend/              # FastAPI application
│   ├── main.py          # API implementation
│   ├── openapi.yaml     # API specification
│   └── run_server.sh    # Startup script
├── frontend/            # Astro application
│   ├── src/
│   │   ├── layouts/     # Layout components
│   │   ├── pages/       # Route pages
│   │   └── styles/      # CSS/Tailwind
│   └── run_frontend.sh  # Startup script
├── models/              # ML model files
├── data/                # Training data
└── run_fullstack.sh     # Start everything
```

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `frontend/package.json` | Node dependencies |
| `backend/main.py` | API server |
| `frontend/src/pages/predict.astro` | Quick predict page |
| `frontend/src/pages/custom.astro` | Custom predict page |
| `models/flight_delay_model.pkl` | Trained ML model |
| `models/airports.csv` | Airport reference data |

## 💡 Tips

1. **Both servers must be running** for the app to work
2. **Backend on port 8000**, frontend on 4321
3. Use `/docs` for interactive API testing
4. Check browser console for frontend errors
5. Use `run_fullstack.sh` for easy startup

## 📚 Documentation

- [TODO.md](./TODO.md) - Project roadmap
- [PHASE2_SUMMARY.md](./PHASE2_SUMMARY.md) - Backend details
- [PHASE3_SUMMARY.md](./PHASE3_SUMMARY.md) - Frontend details
- [backend/README.md](./backend/README.md) - API docs
- [frontend/README.md](./frontend/README.md) - UI docs

---

**Need help?** Check the full documentation files for detailed information!
