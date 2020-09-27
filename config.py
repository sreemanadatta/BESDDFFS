"""Google Cloud Storage Configuration."""
from os import environ

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Flask/IntegrationProject/sreemana-sffs-287bd39b3a2a.json"


# Google Cloud Storage
bucketName = environ.get('sreemana-sffs')
bucketFolder = environ.get('sreemana-sffs/FireAlerts')

# Data
localFolder = environ.get('C:/Flask/IntegrationProject/')# -*- coding: utf-8 -*-

