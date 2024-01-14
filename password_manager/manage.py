#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import keyring
import secrets


def check_secrete_key():
    key = keyring.get_password("pm_v1", "sk")
    if key is None:
        key = secrets.token_hex(16)
        keyring.set_password("pm_v1", "sk", key)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'password_manager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    check_secrete_key()
    main()
