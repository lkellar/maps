from maps import app, db
from maps.models import Call


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Call': Call}
