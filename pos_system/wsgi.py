import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')

# Get the Django WSGI application
django_application = get_wsgi_application()

# Wrap with WhiteNoise for static files
application = WhiteNoise(
    django_application,
    root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles'),
    prefix='/static/',
    max_age=31536000  # 1 year cache (recommended)
)

# Optional: Add additional directories if needed
# application.add_files('/path/to/more/static/files', prefix='more-static/')
