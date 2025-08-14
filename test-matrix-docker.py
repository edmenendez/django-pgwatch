#!/usr/bin/env python3
"""
Docker-based test script to run the full CI matrix locally
Each combination runs in its own container for complete isolation
"""

import subprocess
import sys
import tempfile
from pathlib import Path

# Test matrix from CI (excluding unsupported combinations)
MATRIX = [
    ("3.9", "4.2"),
    ("3.10", "4.2"), ("3.10", "5.0"), ("3.10", "5.1"),
    ("3.11", "4.2"), ("3.11", "5.0"), ("3.11", "5.1"), 
    ("3.12", "4.2"), ("3.12", "5.0"), ("3.12", "5.1"),
]

def run_cmd(cmd, cwd=None, capture_output=True):
    """Run command and return success/output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=capture_output, text=True, cwd=cwd, check=True
        )
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout if capture_output else "", e.stderr if capture_output else ""

def create_dockerfile(python_version, django_version):
    """Create Dockerfile for specific Python/Django combination"""
    dockerfile_content = f"""
FROM python:{python_version}-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \\
    pip install Django=={django_version} && \\
    pip install -e .[dev]

# Set environment variables
ENV PYTHONPATH=.
ENV DJANGO_SETTINGS_MODULE=tests.settings
ENV POSTGRES_HOST=host.docker.internal
ENV POSTGRES_PORT=55235
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=test_pgwatch

# Run the full CI pipeline
CMD ["bash", "-c", "\\
    echo 'Running linting...' && \\
    ruff check django_pgwatch tests && \\
    echo 'Checking formatting...' && \\
    ruff format --check django_pgwatch tests && \\
    echo 'Running type checking...' && \\
    mypy django_pgwatch && \\
    echo 'Running Django migrations...' && \\
    python -m django migrate && \\
    echo 'Running tests...' && \\
    pytest -v \\
"]
"""
    return dockerfile_content

def test_combination(python_version, django_version):
    """Test one Python/Django combination in Docker"""
    print(f"\n{'='*60}")
    print(f"Testing Python {python_version} + Django {django_version}")
    print(f"{'='*60}")
    
    # Create temporary dockerfile
    dockerfile_content = create_dockerfile(python_version, django_version)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.dockerfile', delete=False) as f:
        f.write(dockerfile_content)
        dockerfile_path = f.name
    
    try:
        # Build image
        image_name = f"pgwatch-test-py{python_version.replace('.', '')}-dj{django_version.replace('.', '')}"
        print(f"Building Docker image: {image_name}")
        
        build_cmd = f"docker build -f {dockerfile_path} -t {image_name} ."
        success, stdout, stderr = run_cmd(build_cmd, capture_output=False)
        
        if not success:
            print(f"❌ Failed to build image")
            return False
        
        # Run tests in container
        print(f"Running tests in container...")
        docker_run_cmd = f"docker run --rm --network host {image_name}"
        
        success, stdout, stderr = run_cmd(docker_run_cmd, capture_output=False)
        
        if not success:
            print(f"❌ Python {python_version} + Django {django_version} FAILED")
            return False
        else:
            print(f"✅ Python {python_version} + Django {django_version} PASSED")
            return True
            
    finally:
        # Cleanup
        Path(dockerfile_path).unlink(missing_ok=True)
        # Optional: remove image to save space
        # run_cmd(f"docker rmi {image_name}", capture_output=True)

def main():
    """Run all matrix combinations"""
    
    # Check if PostgreSQL is running
    print("Checking PostgreSQL connection...")
    success, _, _ = run_cmd("docker exec pgwatch-postgres psql -U postgres -d test_pgwatch -c 'SELECT 1;'")
    if not success:
        print("❌ PostgreSQL not running. Please start it first:")
        print("docker run --name pgwatch-postgres -d -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=test_pgwatch -p 55235:5432 postgres:15")
        return False
    
    results = {}
    for python_version, django_version in MATRIX:
        success = test_combination(python_version, django_version)
        results[(python_version, django_version)] = success
        
        # Continue with all combinations to get full picture
        if not success:
            print(f"\n⚠️  {python_version} + Django {django_version} failed, continuing with remaining combinations...")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for (py, dj), success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"Python {py} + Django {dj}: {status}")
    
    print(f"\nTotal: {passed}/{total} combinations tested")
    
    if passed == len(results):
        print("🎉 All tested combinations passed!")
        return True
    else:
        print(f"💥 {len(results) - passed} combinations failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)