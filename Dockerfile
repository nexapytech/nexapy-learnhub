# Use official lightweight Python image (Linux-based)
FROM python:3.11-slim

# Prevent Python from writing .pyc files and unbuffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies required for MySQL & building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker caching)
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install the rest of the requirements (Django, mysqlclient, spacy, etc.)
RUN pip install -r requirements.txt

# Copy spaCy model wheel from local folder and install
COPY AI_spacy_models/en_core_web_md-3.6.0-py3-none-any.whl /app/
RUN pip install /app/en_core_web_md-3.6.0-py3-none-any.whl

# Copy all project files into the container
COPY . .

# Expose Django default port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
