"""
Main file for launching Flask application.
"""

from maps import app, db
from maps.models import Call


# define shell context (only used running 'flask shell')
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Call': Call}


if __name__ == '__main__':
    app.run()
