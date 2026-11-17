
#!/usr/bin/env bash
set -o errexit

echo "Creating database migrations..."
python manage.py makemigrations social

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!"
