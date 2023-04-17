# OBB_task
python task for fetching and transforming data.

This is a Python project for fetching data and transforming data and print data. The project includes a main class CityBikeImporter.py, a unit test file test_importer.py, a Dockerfile for containerization, and a requirements.txt file for installing dependencies.

## Installation
### Requirements

    Python 3.10 or higher (mandatory)
    Docker
    
### Setup

    Clone the project repository from GitHub: git clone https://github.com/yourusername/city-bike-importer.git

    Change directory to the project folder: cd city-bike-importer

    Create a virtual environment: python3 -m venv venv

    Activate the virtual environment: source venv/bin/activate

    Install dependencies: pip install -r requirements.txt
    
    
### Running the Application

To run the application, you need to execute running_city_bikes.py file:

``` python running_city_bike.py ```

This will start the application and begin importing data from the CityBikeImporter.

## Running the Tests

To run the unit tests, use the following command:


``` python -m unittest test_importer.py ```


## Docker

You can also run the project using Docker:

    Build the Docker image: docker build -t city-bike-importer .

    Run the Docker container: docker run -it city-bike-importer
