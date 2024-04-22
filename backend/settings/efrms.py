"""
Custom EFTDMS settings
"""

import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environ.Path(__file__) - 3
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

