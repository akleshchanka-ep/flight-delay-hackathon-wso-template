# Flight Delay Hackathon
<!-- REPLACE THE TITLE WITH THE NAME OF THE EXERCISE -->

This repository includes a Copilot hackathon intended to give you practical experience using the tool.

## 🎯 Goal
<!-- ONE SENTENCE ABOUT THE GOAL OF THE EXERCISE -->
Build an application which will allow someone to select the day of the week and arrival airport to see the chance their flight will be delayed by more than 15 minutes.

## ✍️ Programming Languages
<!-- BULLETED LIST OF LANGUAGES INVOLVES -->
- TypeScript / JavaScript
- Python

## 💻 IDE
<!-- OPTIONALLY SPECIFY THE IDEs THAT SHOULD BE USED -->
- Visual Studio
- Visual Studio Code
- JetBrains IDEs

## 🗒️ Guide
<!-- STEP BY STEP INSTRUCTIONS DETAILING HOW TO COMPLETE THE EXERCISE -->
[GitHub Copilot](https://github.com/features/copilot) is your AI pair programmer, built to support you throughout your development experience. As with any new tool, using GitHub Copilot requires learning a few new skills. This project is built to do exactly that, to give you an opportunity to build a project, using the language and tools you typically use, with GitHub Copilot.

> **[Start hacking!](./hackathon.md)**

## Project Status

### ✅ Phase 1: Model Creation - COMPLETE
- Dataset loaded and cleaned from `data/flights.csv`
- Machine learning model trained to predict delays >15 minutes
- Model saved to `models/flight_delay_model.pkl`
- Airport reference data created at `models/airports.csv`

### ✅ Phase 2: API Development - COMPLETE
- FastAPI REST API implemented in `backend/` folder
- OpenAPI 3.0 specification created
- Two main endpoints:
  - `POST /predict` - Flight delay predictions
  - `GET /airports` - Airport list retrieval
- Interactive documentation at `/docs`
- Full testing suite included

### ✅ Phase 3: Frontend - COMPLETE
- Modern web UI built with Astro + TypeScript + DaisyUI 5
- Three pages: Home, Quick Predict, Custom Predict
- Advanced features:
  - Airport search functionality
  - Weekly batch predictions
  - Visual analytics and comparisons
- Full API integration
- Responsive design for all devices

## 🚀 Quick Start

### Run Everything (Recommended)
```bash
# Start both backend and frontend
./run_fullstack.sh
```

Then open:
- **Frontend:** http://localhost:4321
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Run Individually

**Backend Only:**
```bash
cd backend
./run_server.sh
```

**Frontend Only:**
```bash
cd frontend
./run_frontend.sh
```

### First Time Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create virtual environment (if needed):**
```bash
python3 -m venv flight_model_env
source flight_model_env/bin/activate
pip install -r requirements.txt
```

3. **Install frontend dependencies:**
```bash
cd frontend
npm install
```

## 📚 Documentation

- **[TODO.md](./TODO.md)** - Project roadmap and phase tracking
- **[PHASE2_SUMMARY.md](./PHASE2_SUMMARY.md)** - Complete Phase 2 implementation details
- **[PHASE3_SUMMARY.md](./PHASE3_SUMMARY.md)** - Complete Phase 3 implementation details
- **[QUICKSTART_API.md](./QUICKSTART_API.md)** - Quick API reference guide
- **[backend/README.md](./backend/README.md)** - Backend API documentation
- **[frontend/README.md](./frontend/README.md)** - Frontend documentation
- **[backend/openapi.yaml](./backend/openapi.yaml)** - API specification

## Requirements

This project is configured with a [devcontainer](./.devcontainer/devcontainer.json), which can be [run locally](https://code.visualstudio.com/docs/devcontainers/containers) or in a [codespace](https://github.com/features/codespaces). Please refer to the [setup exercise](./content/0-get-started.md) for more information.

The project does assume you are familiar with programming, but is not prescriptive about language or framework choice.

### Dependencies

**Python (Backend):**
```
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.1.0
joblib>=1.2.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
requests>=2.31.0
```

**Node.js (Frontend):**
```
astro@^5.14.8
typescript
tailwindcss@^4.1.15
daisyui@^5.x
htmx.org@^2.0.4
```

## 🎨 Features

### Quick Prediction
- Simple dropdown interface
- Day of week selection
- Origin and destination airports
- Instant results with visual feedback

### Custom Prediction
- Advanced options
- Radio button day selection
- Airport search functionality
- **Weekly Batch Mode:**
  - Predict entire week at once
  - Compare all days side-by-side
  - Best/worst day recommendations
  - Average weekly risk analysis

### Modern UI
- Built with DaisyUI 5 components
- Responsive design (mobile/tablet/desktop)
- Professional corporate theme
- Loading states and error handling
- Interactive visualizations

## 🤝 Contributing
Contributions are warmly welcomed! ✨

To contribute to a public exercise, please refer to our contribution guidelines [here](https://github.com/ps-copilot-sandbox/.github/blob/main/.github/CONTRIBUTING.md).

To create a net new exercise, please use [this repository template](https://github.com/ps-copilot-sandbox/copilot-exercise-template).
