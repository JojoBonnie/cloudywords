# CloudyWords
# Word Cloud Generator

A full-stack application for creating customizable word clouds with AI integration.

## Project Overview

This word cloud generator allows users to create visually appealing word clouds from manually entered text or AI-generated suggestions. It features extensive customization options, high-quality exports, and a user dashboard for managing word cloud history.

### Key Features

- **Word Input Options**:
  - Manual text input
  - AI-generated word suggestions (OpenAI API)
  
- **Customization**:
  - Adjust size, font, colors, density, orientation, and background
  
- **Export Options**:
  - High-resolution PNG or SVG downloads
  
- **User Authentication**:
  - Login with Google or GitHub
  - Optional Multi-Factor Authentication (MFA)
  
- **Dashboard**:
  - View, edit, and regenerate previous word clouds

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: React + Tailwind CSS
- **Database**: PostgreSQL
- **AI Integration**: OpenAI API
- **Cloud Storage**: Azure Blob Storage
- **Authentication**: Django Allauth
- **Deployment**: Docker-ready for cloud platforms

## Setup Instructions

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker and Docker Compose (optional, for containerized setup)
- OpenAI API key
- Azure Blob Storage account
- Google and GitHub OAuth credentials

### Local Development Setup

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd word-cloud-generator
   ```

2. **Backend Setup**:
   ```
   cd backend
   
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Copy environment variables example file and update with your credentials
   cp .env.example .env
   
   # Apply migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   
   # Run development server
   python manage.py runserver
   ```

3. **Frontend Setup**:
   ```
   cd frontend
   
   # Install dependencies
   npm install
   
   # Copy environment variables example file and update as needed
   cp .env.example .env
   
   # Start development server
   npm start
   ```

4. **Docker Setup** (alternative):
   ```
   # Copy environment variables example file and update with your credentials
   cp .env.example .env
   
   # Start the containers
   docker-compose up -d
   
   # Create superuser
   docker-compose exec backend python manage.py createsuperuser
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Admin panel: http://localhost:8000/admin/
