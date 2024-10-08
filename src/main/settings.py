import os
from .settings_base import *

if os.getenv('PRODUCTION_SECRET_KEY'):
    from .settings_production import *

if os.getenv('RDS_HOSTNAME'):
    from .settings_rds import *

if os.getenv('AWS'):
    from .settings_aws import *