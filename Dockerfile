FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY test_importer.py .
COPY running_city_bike.py .
COPY CityBikeImporter.py .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["pytest", "test_importer.py"]

CMD ["python", "running_city_bike.py"]
