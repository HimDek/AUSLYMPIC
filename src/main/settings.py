import os
from .settings_base import *

if os.getenv('POSTGRES_DATABASE'):
    from .settings_postgresql import *

if os.getenv('PRODUCTION_SECRET_KEY'):
    from .settings_production import *

if os.getenv('VERCEL'):
    from .settings_vercel import *
