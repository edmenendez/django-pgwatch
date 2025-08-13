# Contributing to Django PGWatch

Thank you for your interest in contributing to Django PGWatch!

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/edmenendez/django-pgwatch.git
   cd django-pgwatch
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e .[dev]
   # or
   pip install -r requirements-dev.txt
   ```

4. **Set up PostgreSQL for testing:**
   ```bash
   cd example_project
   docker-compose up -d
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=django_pgwatch

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

## Code Quality

We use several tools to maintain code quality:

```bash
# Format code
ruff format django_pgwatch tests

# Check linting
ruff check django_pgwatch tests

# Type checking
mypy django_pgwatch
```

## Testing the Example Project

```bash
cd example_project
python manage.py migrate
python manage.py createsuperuser

# In one terminal:
python manage.py runserver

# In another terminal:
python manage.py pgwatch_listen
```

## Making Changes

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`
3. **Make your changes** with tests
4. **Run the test suite** to ensure everything passes
5. **Submit a pull request** with a clear description

## Pull Request Guidelines

- Include tests for new functionality
- Update documentation if needed
- Follow the existing code style
- Ensure all CI checks pass
- Write clear commit messages

## Reporting Issues

When reporting issues, please include:

- Python and Django versions
- PostgreSQL version
- Complete error traceback
- Minimal code example to reproduce the issue

## Code Style

- Line length: 90 characters
- Use single quotes for strings
- Follow PEP 8 naming conventions
- Include type hints for new code
- Write docstrings for public functions and classes

## Documentation

Documentation is built from the README.md and docstrings. When adding features:

- Update the main README.md
- Add docstrings to new functions/classes
- Update the example project if relevant
- Consider adding examples to the README

## Release Process

Releases are handled by maintainers:

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG (if we add one)
3. Create a GitHub release
4. GitHub Actions will automatically publish to PyPI