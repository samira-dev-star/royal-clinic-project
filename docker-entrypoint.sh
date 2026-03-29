#!/bin/bash
# docker-entrypoint.sh - LF line endings required!
set -e

echo "🚀 Starting Royal Clinic setup..."

# Wait for MySQL to be ready
if [ "$DATABASE" = "mysql" ]; then
    echo "⏳ Waiting for MySQL at ${DB_HOST:-db}:${DB_PORT:-3306}..."
    # Use timeout to avoid infinite loop
    timeout 60 bash -c 'until nc -z ${DB_HOST:-db} ${DB_PORT:-3306}; do sleep 1; done' || {
        echo "❌ Could not connect to MySQL after 60 seconds"
        exit 1
    }
    echo "✅ MySQL is ready!"
fi

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collect static files (for production)
if [ "$COLLECT_STATIC" = "true" ]; then
    echo "📦 Collecting static files..."
    python manage.py collectstatic --noinput --clear
fi

# Create superuser if requested (development only)
if [ "$CREATE_SUPERUSER" = "true" ] && [ "$DEBUG" = "True" ]; then
    echo "👤 Creating superuser: ${DJANGO_SUPERUSER_USERNAME:-admin}..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME:-admin}').exists():
    User.objects.create_superuser(
        username='${DJANGO_SUPERUSER_USERNAME:-admin}',
        email='${DJANGO_SUPERUSER_EMAIL:-admin@royalclinic.com}',
        password='${DJANGO_SUPERUSER_PASSWORD:-admin123}'
    )
    print("✅ Superuser created!")
else:
    print("⚠️ Superuser already exists")
EOF
fi

echo "✅ Setup complete! Starting Django server..."
exec "$@"