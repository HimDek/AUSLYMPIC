from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = [".auslympic.info", ".vercel.app", "now.sh"]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
