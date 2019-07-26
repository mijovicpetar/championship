"""Development config."""

# For showing debug info.
DEBUG = True

# Get environment variables from os.
DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'championship_db'
DB_USER = 'postgres'
DB_PASS = 'root'

# Database connection string.
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)

# http://flask-sqlalchemy.pocoo.org/2.3/config/
SQLALCHEMY_TRACK_MODIFICATIONS = False
