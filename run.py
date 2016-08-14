"""Entrance of the application"""
from Buddy import app
from Buddy.models import initialize, User, create_user

if __name__ == '__main__':
    initialize()
    try:
        create_user(
            'Jason',
            'test@zillow.com',
            'password',
            is_admin=True
        )
    except ValueError:
        pass
    app.run()
