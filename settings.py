import os
from pathlib import Path
import environ


BASE_DIR = Path(__file__).resolve().parent

env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

TOKEN = env('BOT_TOKEN')