# Testing Guide

This document explains how to run tests for the Vaccination Booking System.

## Test Structure

The tests are organized into several files:

- **test_models.py** - Tests for database models (Vaccine, Branch, Appointment, Dose)
- **test_views.py** - Tests for views and HTTP responses
- **test_forms.py** - Tests for form validation
- **test_integration.py** - End-to-end workflow tests

## Running Tests

### Run All Tests
```bash
python manage.py test
```

### Run Tests for a Specific App
```bash
python manage.py test core
```

### Run Tests from a Specific File
```bash
python manage.py test core.tests.test_models
```

### Run a Specific Test Class
```bash
python manage.py test core.tests.test_models.VaccineModelTest
```

### Run a Specific Test Method
```bash
python manage.py test core.tests.test_models.VaccineModelTest.test_vaccine_creation
```

### Run Tests with Verbose Output
```bash
python manage.py test --verbosity=2
```

### Run Tests and Keep Test Database
```bash
python manage.py test --keepdb
```
This speeds up subsequent test runs by reusing the test database.

### Run Tests with Coverage
First install coverage:
```bash
pip install coverage
```

Then run tests with coverage:
```bash
coverage run --source='.' manage.py test core
coverage report
```

Generate HTML coverage report:
```bash
coverage html
```
Then open `htmlcov/index.html` in your browser.

## Test Coverage

Current test coverage includes:

### Models
- ✅ Vaccine model creation and string representation
- ✅ Branch model with JSON fields (opening_hours)
- ✅ Appointment model with user relationships
- ✅ Dose model with appointment linking
- ✅ Model ordering and filtering

### Views
- ✅ Home view (authenticated and anonymous)
- ✅ Signup view and user creation
- ✅ Appointment CRUD operations
- ✅ Dose creation and management
- ✅ Appointment-to-dose linking
- ✅ Profile view and updates
- ✅ Authentication requirements

### Forms
- ✅ CustomUserCreationForm validation
- ✅ AppointmentForm validation
- ✅ DoseForm validation
- ✅ UserProfileForm validation

### Integration Tests
- ✅ Complete booking workflow
- ✅ Dose recording workflow
- ✅ Appointment linking workflow
- ✅ Branch browsing
- ✅ Appointment management
- ✅ Profile management

## Writing New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `*Test` (e.g., `VaccineModelTest`)
- Test methods: `test_*` (e.g., `test_vaccine_creation`)

### Example Test Structure

```python
from django.test import TestCase
from core.models import YourModel

class YourModelTest(TestCase):
    """Test YourModel"""
    
    def setUp(self):
        """Set up test data before each test"""
        self.instance = YourModel.objects.create(
            field1="value1",
            field2="value2"
        )
    
    def test_model_creation(self):
        """Test creating a model instance"""
        self.assertEqual(self.instance.field1, "value1")
        self.assertIsNotNone(self.instance.id)
    
    def tearDown(self):
        """Clean up after each test (optional)"""
        pass
```

## Common Test Patterns

### Testing Views
```python
from django.test import Client
from django.urls import reverse

class MyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_view_response(self):
        response = self.client.get(reverse('view_name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'template.html')
```

### Testing Authentication
```python
def test_login_required(self):
    response = self.client.get(reverse('protected_view'))
    self.assertEqual(response.status_code, 302)  # Redirect to login
```

### Testing Forms
```python
def test_valid_form(self):
    data = {'field': 'value'}
    form = MyForm(data=data)
    self.assertTrue(form.is_valid())
```

## Continuous Integration

To set up CI/CD with GitHub Actions, create `.github/workflows/django-tests.yml`:

```yaml
name: Django Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.12
    
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run Tests
      run: |
        python manage.py test
```

## Troubleshooting

### Database Issues
If you encounter database errors, try:
```bash
python manage.py test --keepdb=False
```

### Import Errors
Make sure you're in the project root directory and your virtual environment is activated.

### Slow Tests
Use `--keepdb` flag and consider running specific test files instead of the entire suite during development.

## Best Practices

1. **Write tests first** (TDD approach when possible)
2. **Keep tests independent** - each test should work in isolation
3. **Use descriptive test names** - clearly state what is being tested
4. **Test edge cases** - not just the happy path
5. **Mock external dependencies** - don't rely on external APIs or services
6. **Keep tests fast** - avoid unnecessary database queries
7. **Maintain test coverage** - aim for >80% coverage

## Additional Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
