Flight Delay App
================

# The plan

## Phase 1: create the model
The data set is in `/data/flights.csv` file.

0. Read and convert the dataset into something usefull to model building
1. Clean the data by identifying null values and replacing them with an appropriate value (zero in this case).
2. Create a model which provides the chances a flight will be delayed by more than 15 minutes for a given day and airport pair.
3. Save the model to a file for use in an external application.
4. Create a new file with the names and associated ids from the dataset of all airports.

## Phase 2: Create and API endpoint for the model
The model what we build in all files around it has been placed in `/models` folder. Lets' move on.
    
1. creating an endpoint to accept the id of the day of week and airport, which calls the model and returns both the chances the flight will be delayed and the confidence percent of the prediction.
2. creating an endpoint which returns the list of airport names and IDs, sorted in alphabetical order.
3. all data is returned as JSON.

## Phase 3: Create a user-friendly frontend for the endpoint

