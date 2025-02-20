import os


"""Configuration settings for the Flask app."""

# Load environment variables from .env file
SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Pinecone configuration
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'resume-index')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
