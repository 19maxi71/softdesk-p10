# Softdesk Project

Softdesk is a project management application built with Django and Django REST Framework. It allows users to create projects, add contributors, create issues, and comment on issues.

## Features

- User authentication and authorization
- Project creation and management
- Contributor management
- Issue tracking
- Commenting on issues

## Installation

### Prerequisites

- Python 3.8+
- pipenv

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/softdesk.git
    cd softdesk
    ```

2. Install dependencies:
    ```bash
    pipenv install
    ```

3. Create a `.env` file and add your environment variables:
    ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    ```

4. Apply migrations:
    ```bash
    pipenv run python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    pipenv run python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    pipenv run python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`
- Use the admin panel at `http://127.0.0.1:8000/admin/` to manage users and projects

## API Documentation

The API documentation is available at `http://127.0.0.1:8000/api/docs/` once the server is running.

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.