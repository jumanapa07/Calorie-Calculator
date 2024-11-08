# Calorie-Calculator

A Django-based application to log food intake, exercises, and track weight goals.

## Features
- **Custom User Model**: Includes weight, height, age, and gender.
- **Food Log**: Tracks food consumed with nutritional details.
- **Exercise Log**: Logs exercise duration and calories burned.
- **Weight Tracking**: Records user’s weight over time.
- **Fitness Plans**: Users can set target weight goals and calorie intake.

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the server**:
    ```bash
    python manage.py runserver
    ```

7. Visit `http://127.0.0.1:8000` to access the app.

## Models

- **CustomUser**: Extends `AbstractUser`, adds fields for weight, height, age, and gender.
- **Food**: Stores food details including calories, fat, protein, etc.
- **FoodLog**: Logs food consumption with quantity and calories.
- **ExerciseLog**: Logs exercises with duration and calories burned.
- **Weight**: Tracks the user's weight over time.
- **Plan**: Represents a user's fitness plan with target weight and calories.

## Admin Panel

- Access the admin panel at `http://127.0.0.1:8000/admin` to manage users and logs.

## Development Setup

- **Python 3.x**
- **Django**
- Database (SQLite by default)
