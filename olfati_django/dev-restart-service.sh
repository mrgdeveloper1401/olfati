#!/bin/bash

sudo systemctl restart nginx.service
sudo systemctl restart django.service
sudo systemctl restart celery-service.service