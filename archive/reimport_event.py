import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dartmoorrunners.settings")
import django
django.setup()

from .models import *

# Events to re-import
