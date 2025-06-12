# Testing Guide for CloudyWords

This document provides instructions on how to run tests for both the backend and frontend of the CloudyWords application.

## Prerequisites

Before running the tests, make sure you have the following installed:

- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

## Backend Tests

The backend tests are written using Django's testing framework. They test the models, API endpoints, and authentication functionality.

### Running Backend Tests

To run the backend tests, use the following command:

```bash
run_backend_tests.bat
```

This will:
1. Activate the Python virtual environment
2. Run the Django test command

### Backend Test Files

- `backend/core/tests.py`: Tests for the core models (UserProfile, UserCredit, WordCloud)
- `backend/wordcloud_api/tests.py`: Tests for the WordCloud API endpoints
- `backend/authentication/tests.py`: Tests for the authentication API endpoints

## Frontend Tests

The frontend tests are written using Jest and React Testing Library. They test the API services and React components.

### Running Frontend Tests

To run the frontend tests, use the following command:

```bash
run_frontend_tests.bat
```

This will run the Jest test runner in watch mode, which will automatically re-run tests when files change.

### Frontend Test Files

- `frontend/src/services/api.test.js`: Tests for the API service functions
- `frontend/src/contexts/AuthContext.test.js`: Tests for the authentication context

## Running All Tests

To run both backend and frontend tests, use the following command:

```bash
run_all_tests.bat
```

This will run the backend tests first, followed by the frontend tests.

## Adding New Tests

### Adding Backend Tests

To add new backend tests:

1. Create a new `tests.py` file in the app directory or add tests to an existing file
2. Write test classes that inherit from `django.test.TestCase`
3. Write test methods that start with `test_`

Example:

```python
from django.test import TestCase
from django.contrib.auth.models import User

class MyModelTest(TestCase):
    def setUp(self):
        # Set up test data
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_my_feature(self):
        # Test code here
        self.assertEqual(1 + 1, 2)
```

### Adding Frontend Tests

To add new frontend tests:

1. Create a new `.test.js` file next to the file you want to test
2. Write test cases using Jest and React Testing Library

Example:

```javascript
import React from 'react';
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders my component', () => {
  render(<MyComponent />);
  const element = screen.getByText(/my component/i);
  expect(element).toBeInTheDocument();
});
```

## Continuous Integration

It's recommended to set up a CI/CD pipeline to automatically run these tests on every push to the repository. This can be done using GitHub Actions, GitLab CI, or other CI/CD platforms.