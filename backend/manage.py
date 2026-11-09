"""Start the EduBuild Django command-line utility."""

import os
import sys


def main():
    """Start Django and pass along the command typed in the terminal.

    For example, ``python manage.py runserver`` reaches this function,
    which then asks Django to start its development web server.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edubuild.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
