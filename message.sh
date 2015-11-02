#!/bin/bash
python manage.py count_objects apps.hello 2> $(date +%d-%m-%y).dat