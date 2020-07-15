#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Development")

    from configurations.management import execute_from_command_line

    print('DJANGO_CONFIGURATION', os.environ.get('DJANGO_CONFIGURATION'))
    print('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE'))

    execute_from_command_line(sys.argv)
