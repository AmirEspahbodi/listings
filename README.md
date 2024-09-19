# Listings App

A full-featured listings application where users can authenticate, create, edit, and delete their listings. Users can also view listings from all other users. The app is built using **FastAPI**, **Pydantic**, **SQLAlchemy**, and **PostgreSQL**, with **JWT** for secure authentication.

## Features

- **Authentication**: Secure authentication using JWT tokens.
- **User Listings**: Users can create, edit, and delete their listings.
- **FastAPI**: Lightning-fast Python framework for building APIs.
- **SQLAlchemy**: ORM for database interactions.
- **PostgreSQL**: Reliable and robust database management.

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Authentication**: JWT (JSON Web Tokens)
- **Deployment**: Docker

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/listings-app.git
    cd listings-app
    ```

2. Set up your virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database:
    ```bash
    CREATE DATABASE listings_app;
    ```

5. Configure environment variables:
    Create a `.env` file in the project root with the following variables:
    ```env
    DATABASE_URL=postgresql://user:password@localhost/listings_app
    JWT_SECRET_KEY=your-secret-key
    ```

6. Apply database migrations:
    ```bash
    alembic upgrade head
    ```

7. Run the application:
    ```bash
    sudo docker build .
    sudo docker-compose up -d
    sudo docker-compose exec web python3 -m scripts.on_start
    sudo docker-compose exec web python3 -m pytest app/tests/
    ```


