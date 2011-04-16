#!/usr/bin/env python

IMPORT_ERROR = """\
Error: Can't find the file 'settings.py' in the directory containing %r.
It appears you've customized things.
You'll have to run django-admin.py, passing it your settings module.
(If the file settings.py does indeed exist, \
it's causing an ImportError somehow.)
"""

from django.core.management import execute_manager
try:
    import settings  # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write(IMPORT_ERROR % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
