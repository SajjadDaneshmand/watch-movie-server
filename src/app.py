from flask import (
    Flask, redirect, url_for, request, session, flash, render_template, send_file
)

import functools
import os

# Internal
from tools import os_detector
from settings import Settings


configs = Settings()
msg = Settings('msg')


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=configs.SECRET_KEY,
    )
    return app


app = create_app()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))

        return view(**kwargs)
    return wrapped_view


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == configs.password:
            session['user_id'] = True
            return redirect(url_for('files'))
        else:
            flash(msg.pass_error)
            return redirect(request.url)
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def files():
    if os_detector() == 'linux':
        path = configs.linux_path
    elif os_detector() == 'android':
        path = configs.android_path
    else:
        raise Exception('os not detected!')

    file_listdir = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    dir_listdir = [file for file in os.listdir(path) if os.path.isdir(os.path.join(path, file))]

    if request.method == 'POST':
        if request.form['filenames'] in file_listdir:
            filename = request.form['filenames']
            complete_path_file = os.path.join(configs.linux_html_path, filename)
            return render_template('film.html', path=complete_path_file)
        elif request.form['filenames'] in dir_listdir:
            pass  # TODO: complete directory management

    return render_template('files.html', files=file_listdir, dirs=dir_listdir)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

