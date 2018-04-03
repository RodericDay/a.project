import functools
import os
import pathlib
import sqlite3

import bottle


def query(function):
    db = pathlib.Path(os.environ['DATABASE']).resolve()

    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        connection = sqlite3.connect(str(db))
        cursor = connection.cursor()
        with connection:
            data = bottle.request.json or {}
            bottle.request.environ['bottle.request.json'] = None
            output = function(cursor, *args, **kwargs, **data)
        connection.close()
        return output

    return wrapped


@query
def prepare_database(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS records (entry text)")


@bottle.get('/api/stuff/')
@query
def get(cursor):
    cursor.execute("SELECT * FROM records")
    return {"stuff": cursor.fetchall()}


@bottle.post('/api/stuff/')
@query
def post(cursor, hi):
    cursor.execute("INSERT INTO records VALUES (:hi)", locals())
    cursor.connection.commit()
    return get()


@bottle.get('/')
@bottle.get('/<file:path>')
def static(file='index.html'):
    root = pathlib.Path(__file__, '../../../client/static/').resolve()
    return bottle.static_file(file, root=str(root))


prepare_database()
app = bottle.default_app()


if __name__ == '__main__':
    app.run(port=8000, debug=True, reloader=True, quiet=True)
