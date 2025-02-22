FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it script and make it executable
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

# Copy remaining project files
COPY . .

# Fix the command syntax
CMD ./wait-for-it.sh db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000 