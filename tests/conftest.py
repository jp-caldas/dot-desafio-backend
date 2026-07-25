import os
import sys

import django
from decouple import config

os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

# Use test DB in memory
os.environ["DATABASE_URL"] = "sqlite:///test.db"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()


def pytest_configure():
    pass