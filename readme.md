# Personalized Parent Onboarding System with Blog and Vlog Storage

## Overview
This project is a backend system for a personalized onboarding experience for parents. It collects essential details about the parent and their child, and provides a personalized home feed consisting of a mix of blogs and vlogs based on the child's age, gender, and the parent's type (e.g., first-time parent, experienced parent). The system supports CRUD operations for users, children, blogs, and vlogs, and uses JWT for authentication.

## Features
- User registration and authentication using JWT
- CRUD operations for users, children, blogs, and vlogs
- Personalized home feed based on child's age, gender, and parent's type
- Secure API endpoints with permission checks

## Requirements
- Python 3.x
- Django 3.x or later
- Django REST Framework
- Django Simple JWT

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/parent-onboarding-system.git
    cd parent-onboarding-system
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Postman Link
[Postman](https://grey-moon-811508.postman.co/workspace/My-Workspace~2d9e1d64-7e44-40e8-80ea-f093ea6f8db9/collection/23862377-17ada431-aaaf-496e-bf63-fa903da43989?action=share&creator=23862377)

### Authentication
- **Register**: `api/register/`
- **Login**: `/api/token/`
- **Logout**: `api/logout/`

### User Profiles
- **List**: `/api/userprofiles/`
- **Detail**: `/api/userprofiles/<id>/`
- **Update**: `/api/userprofiles/<id>/`
- **Delete**: `/api/userprofiles/<id>/`

### Children
- **List**: `/api/children/`
- **Detail**: `/api/children/<id>/`
- **Update**: `/api/children/<id>/`
- **Delete**: `/api/children/<id>/`

### Blogs
- **List**: `/api/blogs/`
- **Detail**: `/api/blogs/<id>/`
- **Update**: `/api/blogs/<id>/`
- **Delete**: `/api/blogs/<id>/`

### Vlogs
- **List**: `/api/vlogs/`
- **Detail**: `/api/vlogs/<id>/`
- **Update**: `/api/vlogs/<id>/`
- **Delete**: `/api/vlogs/<id>/`

### Home Feed
- **Home Feed**: `api/home-feed/`
- **Detail**: `api/detail/`

## Running Tests
To run the tests, use the following command:
```bash
python manage.py test
```


