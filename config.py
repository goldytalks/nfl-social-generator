"""
Configuration settings for NFL Social Content Generator
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Movement analysis settings
MOVEMENT_THRESHOLD = 2.0  # Minimum % change to be considered a "mover"
TOP_N_MOVERS = 10  # How many movers to analyze

# Tweet generation settings
TWEET_VARIATIONS = 3  # Number of draft versions per mover
INCLUDE_EMOJIS = True  # Toggle emoji usage
CHARACTER_LIMIT = 280  # Tweet length limit

# NFL Data Source Priority (for Phase 2)
NFL_DATA_SOURCES = [
    "sdql",  # Preferred if available
    "espn_api",
    "api_football",
    "web_scraping"  # Fallback
]

# File upload settings
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'data/uploads')
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Export settings
EXPORT_FOLDER = os.getenv('EXPORT_FOLDER', 'data/exports')

# Flask settings - Use environment variables in production
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Get configuration dictionary
def get_config():
    """Return configuration as dictionary"""
    return {
        'movement_threshold': MOVEMENT_THRESHOLD,
        'top_n_movers': TOP_N_MOVERS,
        'tweet_variations': TWEET_VARIATIONS,
        'include_emojis': INCLUDE_EMOJIS,
        'character_limit': CHARACTER_LIMIT,
        'upload_folder': UPLOAD_FOLDER,
        'allowed_extensions': ALLOWED_EXTENSIONS,
        'export_folder': EXPORT_FOLDER
    }
