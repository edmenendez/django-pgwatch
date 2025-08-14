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

4. **Set up PostgreSQL for testing (REQUIRED for tests to pass):**
   
   **Option A: Using Docker (Recommended)**
   ```bash
   # Start PostgreSQL with the exact same settings as CI
   docker run --name pgwatch-postgres -d \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_DB=test_pgwatch \
     -p 5432:5432 \
     postgres:15
   ```
   
   **Option B: Local PostgreSQL Installation**
   ```bash
   # Create user and database (if using local PostgreSQL)
   createuser -s postgres  # Create postgres superuser role
   createdb test_pgwatch -O postgres
   ```
   
   **Option C: Using Docker Compose (from example project)**
   ```bash
   cd example_project
   docker-compose up -d
   ```

## Running Tests

**IMPORTANT: PostgreSQL must be running first (see setup above)**

```bash
# Run all tests (mirrors CI exactly)
PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings pytest

# Run with coverage
PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings pytest --cov=django_pgwatch

# Run specific test file
PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings pytest tests/test_models.py

# Run with verbose output
PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings pytest -v

# Alternative: Set environment variables first
export PYTHONPATH=.
export DJANGO_SETTINGS_MODULE=tests.settings
pytest  # Now this will work
```

**If tests fail with database errors**, ensure:
1. PostgreSQL is running on port 5432
2. User `postgres` exists with password `postgres` 
3. Database `test_pgwatch` exists
4. Connection settings match `tests/settings.py`

## Code Quality

We use several tools to maintain code quality. **Run these checks before committing** to avoid CI failures:

### Quick Check (run this before every commit)
```bash
# Run all quality checks that mirror CI pipeline
ruff check django_pgwatch tests && ruff format --check django_pgwatch tests && mypy django_pgwatch
```

### Individual Commands
```bash
# Auto-fix formatting
ruff format django_pgwatch tests

# Check linting (with auto-fix option)
ruff check django_pgwatch tests --fix

# Check formatting only (no changes)
ruff format --check django_pgwatch tests

# Type checking
mypy django_pgwatch
```

### Complete Pre-Commit Checklist
Before pushing changes, ensure these all pass:
1. **Tests**: `PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings pytest`
2. **Linting**: `ruff check django_pgwatch tests`
3. **Formatting**: `ruff format --check django_pgwatch tests`
4. **Type checking**: `mypy django_pgwatch`

Or run the one-liner: `PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings pytest && ruff check django_pgwatch tests && ruff format --check django_pgwatch tests && mypy django_pgwatch`

### Optional: Pre-commit Hooks (Recommended)
Install pre-commit hooks to automatically run these checks before each commit:
```bash
pip install pre-commit
pre-commit install
```

Now the checks run automatically on `git commit`. To run manually:
```bash
pre-commit run --all-files
```

## CI Pipeline

Our GitHub Actions workflow runs these exact same checks:

1. **Setup**: Install Python, dependencies, and start PostgreSQL
2. **Linting**: `ruff check` and `ruff format --check`
3. **Type Checking**: `mypy django_pgwatch`
4. **Database Setup**: Run Django migrations
5. **Tests**: `pytest` with coverage
6. **Package Build**: Verify the package builds correctly

**The local commands above mirror the CI pipeline** - if they pass locally, CI should pass.

## Troubleshooting

### Common Issues

**MyPy Errors About Missing Types**
- If you see `Library stubs not installed for "xyz"`, add `# type: ignore` to the import
- For Django model fields, avoid verbose type annotations - our mypy config handles them

**Ruff Import Sorting**
- Run `ruff check --fix` to auto-fix import ordering
- Imports should be: stdlib, third-party, local (with blank lines between)

**MyPy Django Issues**
- Ensure you're using the project's virtual environment
- Our mypy config is optimized for Django - don't make it stricter

**PostgreSQL Connection Errors in Tests**
- Tests need PostgreSQL running (see development setup)
- Check your `POSTGRES_*` environment variables match `tests/settings.py`

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

- **Include tests** for new functionality
- **Run the complete pre-commit checklist** (see Code Quality section above)
- **Update documentation** if needed (README.md, docstrings, etc.)
- **Follow the existing code style** (enforced by ruff)
- **Ensure all CI checks pass** - run the same commands locally first
- **Write clear commit messages** describing the "why" not just the "what"

### Before Submitting Your PR
Run this command and ensure it passes:
```bash
PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings pytest && ruff check django_pgwatch tests && ruff format --check django_pgwatch tests && mypy django_pgwatch
```

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