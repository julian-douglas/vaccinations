# Vaccination Booking System

A comprehensive web-based vaccination booking and management system built with Django. This application allows users to browse vaccination centers, book appointments, track their vaccination history, and manage their health records.

## Features

### For Patients
- **Browse Vaccination Centers**: View all available branches with opening hours, contact information, and locations
- **Book Appointments**: Select vaccines, choose convenient time slots, and book appointments at preferred locations
- **Vaccination History**: Track all doses received with details including vaccine type, date, and location
- **Appointment Management**: View upcoming appointments, edit details, or cancel when necessary
- **User Profile**: Manage personal information and account settings

### For Administrators
- **Vaccine Management**: Add and manage vaccine information including pricing, side effects, and dosage requirements
- **Branch Management**: Configure vaccination centers with opening hours, contact details, and capacity
- **Appointment Tracking**: Monitor all scheduled appointments across all branches
- **User Management**: View and manage registered users

### Technical Features
- **REST API**: Full-featured API for programmatic access to all resources
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Authentication**: Secure user registration and login with password validation
- **Data Validation**: Comprehensive form validation and error handling
- **Automated Seeding**: Initial data population for vaccines and branches
- **Comprehensive Testing**: 115+ automated tests covering all functionality

## Technology Stack

- **Backend**: Django 5.2.7
- **API**: Django REST Framework
- **Database**: SQLite (development), PostgreSQL-compatible
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication system
- **Testing**: Django TestCase, REST Framework APIClient

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd vaccinations
```

### 2. Create and Activate Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Run migrations to set up the database:

```bash
python manage.py migrate
```

### 5. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 6. Load Initial Data (Optional)

The system will automatically seed initial vaccine and branch data on first run. To manually trigger seeding:

```bash
python manage.py shell
>>> from core.seed import seed_initial
>>> seed_initial(verbose=True)
```

## Running the Application

### Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

### Access Points

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/
- **API Documentation**: http://127.0.0.1:8000/api/health/

## Usage Guide

### Creating an Account

1. Navigate to the homepage
2. Click "Sign Up" or "Register"
3. Fill in your details (username, email, first name, last name, password)
4. Submit the form
5. You'll be automatically logged in

### Booking an Appointment

1. Log in to your account
2. Click "Book Appointment" or navigate to `/appointments/add/`
3. **Step 1**: Select a branch from the list
4. **Step 2**: Choose a vaccine
5. **Step 3**: Pick a date and time
6. **Step 4**: Add any notes (optional)
7. Review and confirm your appointment

### Recording a Dose

1. Navigate to "Dose History" from your profile
2. Click "Add Dose"
3. Option A: Link to an existing appointment
4. Option B: Manually enter dose details
5. Submit the form

### Managing Appointments

- **View Appointments**: Navigate to `/appointments/`
- **Edit Appointment**: Click "Edit" next to any upcoming appointment
- **Cancel Appointment**: Click "Delete" and confirm

## API Usage

### Authentication

The API currently allows open access. To restrict endpoints, add authentication classes to `core/api_views.py`.

### Available Endpoints

**Vaccines**
```bash
GET    /api/vaccines/          # List all vaccines
GET    /api/vaccines/{id}/     # Get vaccine details
```

**Branches**
```bash
GET    /api/branches/          # List all branches
GET    /api/branches/{id}/     # Get branch details
```

**Appointments** (requires authentication in production)
```bash
GET    /api/appointments/      # List appointments
POST   /api/appointments/      # Create appointment
GET    /api/appointments/{id}/ # Get appointment details
PUT    /api/appointments/{id}/ # Update appointment
DELETE /api/appointments/{id}/ # Delete appointment
```

**Doses** (requires authentication in production)
```bash
GET    /api/doses/             # List doses
POST   /api/doses/             # Create dose
GET    /api/doses/{id}/        # Get dose details
DELETE /api/doses/{id}/        # Delete dose
```

**Users**
```bash
GET    /api/users/             # List users
POST   /api/users/             # Create user
GET    /api/users/{id}/        # Get user details
```

### Example API Requests

**List all vaccines:**
```bash
curl http://127.0.0.1:8000/api/vaccines/
```

**Create an appointment:**
```bash
curl -X POST http://127.0.0.1:8000/api/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "vaccine": 1,
    "branch": 1,
    "datetime": "2024-12-01T10:00:00Z"
  }'
```

## Testing

The application includes a comprehensive test suite with 115+ tests.

### Run All Tests

```bash
python manage.py test core.tests
```

### Run Specific Test Suites

```bash
# Model tests
python manage.py test core.tests.test_models

# View tests
python manage.py test core.tests.test_views

# API tests
python manage.py test core.tests.test_api

# Integration tests
python manage.py test core.tests.test_integration
```

### Code Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test

# View coverage report
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in your browser
```

For more testing information, see [TESTING_QUICKSTART.md](TESTING_QUICKSTART.md) and [TESTING.md](TESTING.md).

## Project Structure

```
vaccinations/
├── config/                  # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── core/                    # Main application
│   ├── migrations/         # Database migrations
│   ├── tests/              # Test suite
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   ├── test_forms.py
│   │   ├── test_integration.py
│   │   ├── test_api.py
│   │   ├── test_model_methods.py
│   │   └── test_signals.py
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── api_views.py        # REST API views
│   ├── forms.py            # Form definitions
│   ├── serializers.py      # API serializers
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   └── seed.py             # Data seeding
├── templates/              # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── appointment_form.html
│   └── ...
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Database Models

### User
Extended Django user model with authentication

### Vaccine
- Name, manufacturer, administration route
- Dosage information (primary series, boosters, recurrence)
- Price per dose
- Side effects (JSON field)
- Age restrictions and contraindications

### Branch
- Name, address, postcode
- Contact information (phone, email)
- Opening hours (JSON field with day/time structure)
- Status calculation (open/closed based on current time)
- Optional image

### Appointment
- Links User, Vaccine, and Branch
- Date and time
- Optional notes
- Creation timestamp
- Ordered by datetime (descending)

### Dose
- Records actual vaccination administered
- Links to User and Vaccine
- Optional link to Appointment
- Date administered and dose number
- Unique constraint on (vaccine, user, dose_number)

## Configuration

### Environment Variables

For production deployment, set these environment variables:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Settings Files

Edit `config/settings.py` for:
- Database configuration
- Static files settings
- Allowed hosts
- Installed apps
- Middleware configuration

## Deployment

### Preparation

1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure static files serving
5. Set a strong `SECRET_KEY`

### Collect Static Files

```bash
python manage.py collectstatic
```

### Database Migration

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### WSGI Server

Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn config.wsgi:application
```

### Recommended Stack

- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: PostgreSQL
- **Hosting**: AWS, Heroku, DigitalOcean, or similar

## Security Considerations

- Change `SECRET_KEY` for production
- Use HTTPS in production
- Enable CSRF protection (enabled by default)
- Use strong password validation (configured)
- Keep dependencies updated
- Add authentication to API endpoints for production
- Configure proper CORS settings if API is used from other domains

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guidelines
- Update documentation as needed
- Ensure all tests pass before submitting PR

## Troubleshooting

### Common Issues

**Database errors after pulling updates:**
```bash
python manage.py migrate
```

**Static files not loading:**
```bash
python manage.py collectstatic
```

**Port already in use:**
```bash
python manage.py runserver 8001  # Use a different port
```

**Module not found:**
```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## Acknowledgments

- Django framework and community
- Django REST Framework
- All contributors to this project

---

**Version**: 1.0.0  
**Last Updated**: November 2024
