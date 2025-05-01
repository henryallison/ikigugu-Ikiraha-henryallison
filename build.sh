#!/usr/bin/env bash
# Exit on error
set -o errexit

# Check Python version and warn if not 3.9 (but continue anyway)
PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [ "$PYTHON_VERSION" != "3.9" ]; then
  echo "Warning: Recommended Python version is 3.9 (found $PYTHON_VERSION)"
  echo "Render uses Python 3.11 by default - we'll install compatible package versions"
fi

# Upgrade pip and setuptools first (essential for Render)
pip install --upgrade pip setuptools wheel

# Install requirements with modern resolver but allow downgrades
pip install \
  --no-cache-dir \
  --upgrade-strategy only-if-needed \
  -r requirements.txt

# Special handling for numpy and related packages
if [ "$PYTHON_VERSION" == "3.9" ]; then
  # If Python 3.9, install exact versions
  pip install "numpy==1.21.6" "scipy==1.7.3" "scikit-learn==1.0.2"
else
  # For Python 3.11 (Render's default), install compatible versions
  pip install "numpy>=1.23.0" "scipy>=1.9.0" "scikit-learn>=1.2.0"
fi

# Verify installed versions
echo "=== Installed Package Versions ==="
pip freeze | grep -E 'numpy|scipy|scikit-learn|Django'

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
