FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g nodemon

COPY nodemon.json .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add this to make the app directory a Python module
ENV PYTHONPATH=/app

CMD ["nodemon", "--legacy-watch", "--verbose", "--exec", "python -u app/main.py"]