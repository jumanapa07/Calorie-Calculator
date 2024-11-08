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
    git clone https://github.com/jumanapa07/Calorie-Calculator.git
    cd Calorie-Calculator
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
   

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
- Database ( MySQL)
- 
## Screenshots

<div align="center">
  <img src="https://github.com/user-attachments/assets/a106dbde-ff3b-4db9-a842-191821d2623f" width="300"/>
  <img src="https://github.com/user-attachments/assets/69ed9f04-b15e-4b4a-a370-33bfbe0873a4" width="300"/>
  <img src="https://github.com/user-attachments/assets/4f515d73-9ca5-4470-b8e1-43b2c9f7a96d" width="300"/>
  <img src="https://github.com/user-attachments/assets/37d6022d-5e8e-41e0-9d65-c8f80c0e5f1f" width="300"/>
  <img src="https://github.com/user-attachments/assets/b4f8168c-9876-4a56-a206-cd66acce54b2" width="300"/>
  <img src="https://github.com/user-attachments/assets/1b463b77-5b92-43bb-a6a2-0fb3f2612424" width="300"/>
  <img src="https://github.com/user-attachments/assets/50cf1815-108d-46c5-a995-ccb7610ed259" width="300"/>
  <img src="https://github.com/user-attachments/assets/87a1fdde-7b09-4222-bc72-1369fcd73eba" width="300"/>
  <img src="https://github.com/user-attachments/assets/1b04ffe0-a0e5-479a-9c87-0b73f182b6b3" width="300"/>
</div>






