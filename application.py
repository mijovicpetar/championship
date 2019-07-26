"""Run app script."""

from app import create_app, DB

application = create_app('prod')

# Create tables in database if tables don't exist.
with application.app_context():
    DB.create_all()

if __name__ == '__main__':
    # Run the app.
    application.run()
