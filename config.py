import os
from dotenv import load_dotenv

# Load environment variables in order of priority:
# 1. user_config.env (user's actual keys)
# 2. my_config.env (user's custom config)
# 3. config.env (fallback with placeholder values)
load_dotenv('user_config.env')
load_dotenv('my_config.env')
load_dotenv('config.env')  # Fallback with placeholder values

class Config:
    """Configuration settings for the Upwork Assistant"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # GitHub API settings
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_API_BASE_URL = 'https://api.github.com'
    
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Application settings
    MAX_REPOS_TO_FETCH = int(os.getenv('MAX_REPOS_TO_FETCH', '10'))
    MAX_PROPOSAL_LENGTH = int(os.getenv('MAX_PROPOSAL_LENGTH', '2000'))
    
    # Database settings (for future use)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///upwork_assistant.db') 