# Cloudy Words - Developer Setup Guide

This guide will help you set up the Cloudy Words project for local development.

## Prerequisites

- Python 3.12+ 
- pip (Python package manager)
- Git

## Initial Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-organization/wordcloud-generator.git
   cd wordcloud-generator
   ```

2. **Create a virtual environment**

   ```bash
   # For Windows
   python -m venv .venv
   .venv\Scripts\activate

   # For macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your configuration
   # At minimum, set DEBUG=True
   ```

5. **Create directory structure**

   The project requires certain directories to exist:

   ```bash
   # Create directories for static and media files
   mkdir -p static/css static/js static/images media
   ```

6. **Initialize the database**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (admin)**

   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**

   ```bash
   python manage.py collectstatic
   ```

## Running the Development Server

```bash
python manage.py runserver
