#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure Python 3.9 is used (recommended for your requirements)
PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [ "$PYTHON_VERSION" != "3.9" ]; then
  echo "Warning: Recommended Python version is 3.9 (found $PYTHON_VERSION)"
fi

# Create and activate virtual environment (if not already in one)
if [ -z "$VIRTUAL_ENV" ]; then
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  # OR for Windows: source venv/Scripts/activate
fi

# Upgrade pip and setuptools first
pip install --upgrade pip setuptools

# Install requirements with legacy resolver for better dependency resolution
pip install \
  --use-deprecated=legacy-resolver \
  --no-cache-dir \
  -r requirements.txt

# Install specific compatible versions of problematic packages
pip install "numpy==1.21.6" "scipy==1.7.3" "scikit-learn==1.0.2"

# Verify installed versions
echo "Verifying installed packages:"
pip freeze | grep -E 'numpy|scipy|scikit-learn'

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
