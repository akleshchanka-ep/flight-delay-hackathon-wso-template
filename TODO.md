Flight Delay App
================

# The plan

## Phase 1: create the model ✅ COMPLETED
The data set is in `/data/flights.csv` file.

0. ✅ Read and convert the dataset into something usefull to model building
1. ✅ Clean the data by identifying null values and replacing them with an appropriate value (zero in this case).
2. ✅ Create a model which provides the chances a flight will be delayed by more than 15 minutes for a given day and airport pair.
3. ✅ Save the model to a file for use in an external application.
4. ✅ Create a new file with the names and associated ids from the dataset of all airports.

## Phase 2: Create and API endpoint for the model ✅ COMPLETED
The model what we build in all files around it has been placed in `/models` folder. Lets' move on.

0. ✅ We are using FastAPI python framework for endpoint creation. Let's keep the "server" code in dedicated folder called "backend" inside the project.
1. ✅ Generate OpenAPI specification for the API what we have from python models. There are should be two endpoints: for predictions and for airports Id's fetching. More info in next steps.
2. ✅ Define an endpoint to accept the id of the day of week and airport, which calls the model and returns both the chances the flight will be delayed and the confidence percent of the prediction.
3. ✅ Define an endpoint which returns the list of airport names and IDs, sorted in alphabetical order.
4. ✅ Based on OpenAPI specification you created implement it using FastAPI python framework.
5. ✅ All data is returned as JSON.

**Phase 2 Implementation Summary:**
- Created `/backend` folder with complete FastAPI application
- Implemented OpenAPI 3.0 specification (`backend/openapi.yaml`)
- Created two main endpoints:
  - `POST /predict` - Predicts flight delay probability
  - `GET /airports` - Returns sorted list of airports with pagination
- Added health check endpoint and interactive documentation
- Updated `requirements.txt` with FastAPI dependencies
- Created test script and documentation

**To run the API server:**
```bash
cd backend
./run_server.sh
```
Or:
```bash
cd backend
uvicorn main:app --reload
```

API will be available at: http://localhost:8000
Interactive docs at: http://localhost:8000/docs

## Phase 3: Create a user-friendly frontend for the endpoint ✅ COMPLETED
Let's finish the task wrapping up everything into nice Web UI.
Technical requirements: TypeScipt based, server-side rendering using Astro + HTMX. Nice modern Web UI based on DaisyUI 5 framework. Put all fontend related code in `frontend` folder. 

Here are the steps:
0. ✅ create dedicated `/frontend` folder for the all front-end related code
1. ✅ Check the server OpenAPI specification in `backend/openapi.yaml` file.
2. ✅ Strat building fontend based on the API file
3. ✅ From UI perspective we should have main screen with options for regular (default) prediction and for custome one with additional inputs. Those types of predicions might be places into different pages what available from mains screen.
4. ✅ Test ui.
5. ✅ Create sh scripts to start the frontend and backend + frontend all togheter.

**Phase 3 Implementation Summary:**
- Created `/frontend` folder with complete Astro + TypeScript project
- Implemented three pages:
  - Home page (`/`) with navigation
  - Quick Predict page (`/predict`) for simple predictions
  - Custom Predict page (`/custom`) with advanced features including weekly batch predictions
- Integrated with backend API:
  - `GET /airports` for airport list
  - `POST /predict` for delay predictions
- Applied DaisyUI 5 components throughout
- Created startup scripts:
  - `frontend/run_frontend.sh` - Start frontend only
  - `run_fullstack.sh` - Start both backend and frontend
- Added comprehensive documentation in `frontend/README.md`

**To run the complete application:**
```bash
./run_fullstack.sh
```

Frontend: http://localhost:4321
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs