import logging
import functools
import sqlite3
from bottle import route, run, debug, jinja2_view, request

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
view = functools.partial(jinja2_view, template_lookup=['templates'])


@route('/todo')
@view('make_table.html')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    conn.close()
    return {'rows': result}


@route('/new', method='GET')
@view('new_task.html')
def new_item():
    if request.GET.get('save', '').strip():  # pylint: disable=no-member
        new = request.GET.get('task', '').strip()  # pylint: disable=no-member
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('INSERT INTO todo(task, status) VALUES(?,?)', (new, 1))
        new_id = c.lastrowid
        conn.commit()
        c.close()
        return '<p>The new task was inserted into the database, the id is %s</p>' % new_id
    else:
        return {}


@route('/edit/<no:int>', method='GET')
@view('edit_task.html')
def edit_item(no):
    if request.GET.get('save', '').strip():  # pylint: disable=no-member
        edit = request.GET.get('task', '').strip()  # pylint: disable=no-member
        status = request.GET.get('status', '').strip()  # pylint: disable=no-member
        if status == 'open':
            status = 1
        else:
            status = 0
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('UPDATE todo SET task = ?, status = ? WHERE id LIKE ?', (edit, status, no))
        conn.commit()
        return '<p>The item number %s was successfully updated</p>' % no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('SELECT task FROM todo WHERE id LIKE ?', str(no))
        cur_data = c.fetchone()
        return {'old': cur_data[0], 'no': no}


def main():
    debug(True)
    run(reloader=True, host='localhost', port=8080)

if __name__ == '__main__':
    main()
