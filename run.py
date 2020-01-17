"""
Main file for launching Flask application.
"""

from maps import app, db, cli
from maps.models import Call


cli.register(app.cli)

# define shell context (only used running 'flask shell')
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Call': Call}


if __name__ == '__main__':
    app.run()
